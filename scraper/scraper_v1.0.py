import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration settings
CONFIG = {
    "USERNAME": "username",
    "PASSWORD": "password",
    "LOGIN_URL": "https://www.orchidroots.com/login/?next=/",
    "BASE_URL": "https://www.orchidroots.com/orchidaceae/hybrid/?app=orchidaceae&role=pri&family=Orchidaceae&genus=Cattleya",
    "LOGOUT_URL": "https://orchidroots.com/logout/?next=/",
    "HEADLESS_MODE": False,  # Set to True for headless mode
    "CHROME_DRIVER_PATH": r"C:/path/to/chromedriver/chromedriver.exe",
    "IMAGE_DIR": "orchid_images",
    #"ROWS_PER_PAGE": 5,
    "PAGE_LOAD_WAIT": 5,
    "NEXT_PAGE_WAIT": 5,
    "IMAGE_DOWNLOAD_WAIT": 3,
    "LIGHTBOX_CLOSE_WAIT": 2,
    "RETRY_WAIT": 2,
    "MAX_RETRIES": 5
}

# Set up Selenium WebDriver
options = Options()
options.headless = CONFIG["HEADLESS_MODE"]
service = Service(CONFIG["CHROME_DRIVER_PATH"])
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, CONFIG["PAGE_LOAD_WAIT"])

# Ensure image directory exists
if not os.path.exists(CONFIG["IMAGE_DIR"]):
    os.makedirs(CONFIG["IMAGE_DIR"])

# Function to check if user is logged in
def is_logged_in():
    driver.get(CONFIG["BASE_URL"])
    time.sleep(CONFIG["PAGE_LOAD_WAIT"])
    return "login" not in driver.current_url.lower()

# Function to log in
def login():
    driver.get(CONFIG["LOGIN_URL"])
    
    if is_logged_in():
        logging.info("Already logged in. Proceeding...")
        return

    logging.info("Logging in...")
    
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(CONFIG["USERNAME"])
    driver.find_element(By.NAME, "password").send_keys(CONFIG["PASSWORD"])
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(CONFIG["PAGE_LOAD_WAIT"])

    if not is_logged_in():
        logging.error("Login failed!")
        driver.quit()
        exit()
    else:
        logging.info("Login successful!")

# Function to scrape the current page
def scrape_index_page():
    data = []
    page_number = 1

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table_rows = soup.select("table tbody tr")

        for row in table_rows:  # Only process first N rows per page
            cols = row.find_all("td")
            if len(cols) < 8:
                continue

            grex_link_tag = cols[0].find("a")
            grex_name = grex_link_tag.text.strip() if grex_link_tag else cols[0].text.strip()
            grex_link = f"https://www.orchidroots.com{grex_link_tag['href']}" if grex_link_tag and grex_link_tag.get("href") else "N/A"

            parentage_elements = [p.get_text(strip=True) for p in cols[1].find_all(["a", "span"]) if p.get_text(strip=True)]
            parentage_text = " × ".join(parentage_elements)

            if "Synonym of" in cols[1].text:
                parentage_text = f"Synonym of {parentage_text}"

            data.append({
                "Grex Name": grex_name,
                "Grex Link": grex_link,
                "Parentage": parentage_text,
                "Registrant": cols[2].text.strip(),
                "Originator": cols[3].text.strip(),
                "Year": cols[4].text.strip(),
                "Ancestors": cols[5].text.strip(),
                "Descendants": cols[6].text.strip(),
                "Images": cols[7].text.strip()
            })

        # Click "Next" if available
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_button.get_attribute("class").lower():
                logging.info(f"No more pages to scrape. Total pages: {page_number}")
                break  
            next_button.click()
            time.sleep(CONFIG["NEXT_PAGE_WAIT"])
            page_number += 1
        except:
            logging.info("No 'Next' button found. Stopping.")
            break  

    return data

# Function to navigate through alphabetical letters
def click_through_letters():
    global all_scraped_data  # Ensure we're storing all scraped data

    # Scrape "A" first since it's already active
    logging.info("Scraping initial letter: A")
    scraped_data = scrape_index_page()
    all_scraped_data.extend(scraped_data)

    while True:
        try:
            letter_links = driver.find_elements(By.CSS_SELECTOR, "body > div.justify-content-left.align-items-center > div > div:nth-child(3) > div:nth-child(2) > ul > li")[1:-1]  # Skip "A" and "All"

            for i in range(len(letter_links)):  
                try:
                    # Re-fetch elements dynamically
                    letter_links = driver.find_elements(By.CSS_SELECTOR, "body > div.justify-content-left.align-items-center > div > div:nth-child(3) > div:nth-child(2) > ul > li")[1:-1]
                    letter = letter_links[i]

                    logging.info(f"Clicking on letter: {letter.text}")

                    # Scroll into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", letter)
                    time.sleep(CONFIG["LIGHTBOX_CLOSE_WAIT"])

                    # Wait for the element to be clickable
                    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, letter.text)))

                    # Click the letter
                    ActionChains(driver).move_to_element(letter).click().perform()

                    time.sleep(CONFIG["PAGE_LOAD_WAIT"])  # Allow page to load

                    # Scrape after clicking
                    scraped_data = scrape_index_page()
                    all_scraped_data.extend(scraped_data)

                except (StaleElementReferenceException, ElementClickInterceptedException):
                    logging.warning(f"Retrying click for letter {letter.text} due to exception.")
                    time.sleep(CONFIG["RETRY_WAIT"])  

            break  

        except Exception as e:
            logging.error(f"Error navigating through letters: {e}")
            time.sleep(CONFIG["RETRY_WAIT"])

# Function to scrape species data
def scrape_species():
    species_data = []
    
    try:
        show_species_button = WebDriverWait(driver, CONFIG["PAGE_LOAD_WAIT"]).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Show species"))
        )
        show_species_button.click()
        time.sleep(CONFIG["PAGE_LOAD_WAIT"])
    except Exception as e:
        logging.error("Error clicking 'Show species':", e)
        return species_data

    try:
        all_button = WebDriverWait(driver, CONFIG["PAGE_LOAD_WAIT"]).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "All"))
        )
        all_button.click()
        time.sleep(CONFIG["PAGE_LOAD_WAIT"])
    except Exception as e:
        logging.error("Error clicking 'All':", e)
        return species_data

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table_rows = soup.select("table tbody tr")

        if not table_rows:
            break

        # Process each row
        for row in table_rows:
            cells = row.find_all("td")
            
            if len(cells) >= 7:
                # Extract species name and link
                species_link_tag = cells[0].find("a")
                species_name = species_link_tag.text.strip() if species_link_tag else cells[0].text.strip()
                species_link = f"https://www.orchidroots.com{species_link_tag['href']}" if species_link_tag and species_link_tag.get("href") else "N/A"

                author = cells[1].text.strip()
                year = cells[2].text.strip()
                subgeneric_ranks = cells[3].text.strip()
                distribution = cells[4].text.strip()
                descendants = cells[5].text.strip()
                photos = cells[6].text.strip()

                species_data.append({
                    "Binomial": species_name,
                    "Species Link": species_link,
                    "Author": author,
                    "Year": year,
                    "Subgeneric Ranks": subgeneric_ranks,
                    "Distribution": distribution,
                    "# Descendants": descendants,
                    "# Photos": photos
                })

        # Click "Next" if available
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")  
            if "disabled" in next_button.get_attribute("class").lower():
                logging.info("No more species pages to scrape.")
                break
            next_button.click()
            time.sleep(CONFIG["NEXT_PAGE_WAIT"])
        except:
            logging.info("No 'Next' button found for species. Stopping.")
            break

    return species_data

# Function to download all images from species links
def download_images_species(species_data):
    for species in species_data:
        species_link = species["Species Link"]
        num_photos = int(species["# Photos"]) if species["# Photos"].isdigit() else 0
        if species_link == "N/A" or num_photos == 0:
            logging.info(f"Skipping {species['Binomial']} as it has no images.")
            continue

        driver.get(species_link)
        time.sleep(CONFIG["PAGE_LOAD_WAIT"])  # Allow page to load

        try:
            # Find all image thumbnails
            thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.box a img")

            if not thumbnails:
                logging.info(f"No images found for {species['Binomial']}")
                continue

            for idx, thumb in enumerate(thumbnails):
                try:
                    thumb.click()
                    time.sleep(CONFIG["IMAGE_DOWNLOAD_WAIT"])  # Wait for full-size image to load

                    # Locate full-size image
                    full_image = driver.find_element(By.CSS_SELECTOR, "#lightbox img")
                    image_url = full_image.get_attribute("src")

                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_path = os.path.join(CONFIG["IMAGE_DIR"], f"{species['Binomial'].replace(' ', '_')}_{idx+1}.jpg")
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        logging.info(f"Downloaded {species['Binomial']} image {idx+1} to {image_path}")
                    else:
                        logging.error(f"Failed to download image {idx+1} for {species['Binomial']}")

                    # Close lightbox (press Escape key)
                    ActionChains(driver).send_keys("\ue00c").perform()
                    time.sleep(CONFIG["LIGHTBOX_CLOSE_WAIT"])
                    
                except Exception as e:
                    logging.error(f"Error downloading image {idx+1} for {species['Binomial']}: {e}")

        except Exception as e:
            logging.error(f"Error processing {species['Binomial']}: {e}")

# Function to download all images from grex links
def download_images_grexs(hybrid_data):
    for hybrid in hybrid_data:
        grex_link = hybrid["Grex Link"]
        num_images = int(hybrid["Images"]) if hybrid["Images"].isdigit() else 0
        if grex_link == "N/A" or num_images == 0:
            logging.info(f"Skipping {hybrid['Grex Name']} as it has no images.")
            continue

        driver.get(grex_link)
        time.sleep(CONFIG["PAGE_LOAD_WAIT"])  # Allow page to load

        try:
            # Find all image thumbnails
            thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.box a img")

            if not thumbnails:
                logging.info(f"No images found for {hybrid['Grex Name']}")
                continue

            for idx, thumb in enumerate(thumbnails):
                try:
                    thumb.click()
                    time.sleep(CONFIG["IMAGE_DOWNLOAD_WAIT"])  # Wait for full-size image to load

                    # Locate full-size image
                    full_image = driver.find_element(By.CSS_SELECTOR, "#lightbox img")
                    image_url = full_image.get_attribute("src")

                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_path = os.path.join(CONFIG["IMAGE_DIR"], f"{hybrid['Grex Name'].replace(' ', '_')}_{idx+1}.jpg")
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        logging.info(f"Downloaded {hybrid['Grex Name']} image {idx+1} to {image_path}")
                    else:
                        logging.error(f"Failed to download image {idx+1} for {hybrid['Grex Name']}")

                    # Close lightbox (press Escape key)
                    ActionChains(driver).send_keys("\ue00c").perform()
                    time.sleep(CONFIG["LIGHTBOX_CLOSE_WAIT"])
                    
                except Exception as e:
                    logging.error(f"Error downloading image {idx+1} for {hybrid['Grex Name']}: {e}")

        except Exception as e:
            logging.error(f"Error processing {hybrid['Grex Name']}: {e}")

# Main function
def main():
    global all_scraped_data
    all_scraped_data = []
    
    try:
        login()
        
        driver.get(CONFIG["BASE_URL"])
        click_through_letters()
        hybrids = all_scraped_data.copy()
        
        species = scrape_species()

        download_images_species(species)  # Downloads images from species
        download_images_grexs(hybrids)    # Downloads images from grex links

    except Exception as e:
        logging.error(f"An error occurred during the main execution: {e}")
    finally:
        driver.quit()

    # Save data to CSV
    hybrid_df = pd.DataFrame(hybrids)
    species_df = pd.DataFrame(species)

    hybrid_df.to_csv("orchidroots_cattleya_hybrids.csv", index=False)
    species_df.to_csv("orchidroots_cattleya_species.csv", index=False)

    pd.set_option('display.max_colwidth', None)

    logging.info("Hybrids Data:")
    logging.info(hybrid_df)
    logging.info("\nSpecies Data:")
    logging.info(species_df)

if __name__ == "__main__":
    main()
