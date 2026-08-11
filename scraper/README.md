# Scraper

`scraper_v1.0.py` is the Selenium + BeautifulSoup scraper used to collect the source data for
this project from [orchidroots.com](https://www.orchidroots.com/) on 12 March 2025. It walks
the *Cattleya* hybrid index letter by letter, then the species index, and writes
`orchidroots_cattleya_hybrids.csv` and `orchidroots_cattleya_species.csv`.

It is vendored here so the analysis and its provenance stay in one place. It also lives in its
own repository, [`musharna/OrchidRootsScraper`](https://github.com/musharna/OrchidRootsScraper).

**The output of this script is not distributed in this repository.** `data/` contains only
derived aggregates — see [`../data/README.md`](../data/README.md) for why.

## Running it

You will need to fill in the `CONFIG` block at the top: an orchidroots account, and a path to a
`chromedriver` matching your installed Chrome. The committed values are placeholders.

```python
CONFIG = {
    "USERNAME": "username",
    "PASSWORD": "password",
    "CHROME_DRIVER_PATH": r"C:/path/to/chromedriver/chromedriver.exe",
    ...
}
```

Requires `selenium`, `beautifulsoup4`, `pandas` and `requests`.

## Before you run it

- The script as written also downloads every species and grex photograph
  (`download_images_species`, `download_images_grexs`). Those images are third-party
  copyrighted works. Comment out both calls in `main()` unless you specifically need them.
- The waits in `CONFIG` (`PAGE_LOAD_WAIT`, `NEXT_PAGE_WAIT`) double as rate limiting. Do not
  lower them. A full run takes hours by design.
- orchidroots republishes the RHS International Orchid Register. Scraping it for research is
  one thing; redistributing a substantial part of it is another — see
  [`../data/README.md`](../data/README.md).
