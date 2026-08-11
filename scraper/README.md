# Scraper

`scraper_v1.0.py` is the Selenium and BeautifulSoup scraper used to collect the source data for this
project from [orchidroots.com](https://www.orchidroots.com/) on 12 March 2025. It walks the
*Cattleya* hybrid index letter by letter, then the species index, and writes
`orchidroots_cattleya_hybrids.csv` and `orchidroots_cattleya_species.csv`.

It is vendored here so that the analysis and its provenance stay in one place. It also lives in its
own repository, [`musharna/OrchidRootsScraper`](https://github.com/musharna/OrchidRootsScraper).

The output of this script is not distributed in this repository. `data/` contains only derived
aggregates, and [`../data/README.md`](../data/README.md) explains why.

## Running it

You will need to fill in the `CONFIG` block at the top with an orchidroots account and a path to a
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

As written, the script also downloads every species and grex photograph, through
`download_images_species` and `download_images_grexs`. Those images are third-party copyrighted
works, so comment out both calls in `main()` unless you specifically need them.

The waits in `CONFIG`, `PAGE_LOAD_WAIT` and `NEXT_PAGE_WAIT`, double as rate limiting and should not
be lowered. A full run takes hours by design.

orchidroots republishes the RHS International Orchid Register. Scraping it for research is one
thing and redistributing a substantial part of it is another, as discussed in
[`../data/README.md`](../data/README.md).
