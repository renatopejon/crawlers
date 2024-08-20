# Bahrain Tender Board web crawler
This crawler scrape all the public tenders available on the [Kingdom of Bahrain Tender Board](https://www.tenderboard.gov.bh/Tenders/Public%20Tenders/) and save it to a SQLite database

## Project
This project was made using [Scrapy](https://github.com/scrapy/scrapy): to run the spider just:
```bash
scrapy crawl tenderspider
```

### Data scraped
The following data are scraped from each tender:

- Number
- Subject
- Reference Number
- Description
- Issued by
- Category
- Type
- Initial Bond
- Bid validity
- Fee
- Contract Duration
- Publish date
- Purchase date
- Opening date
- Closing date

### Avoiding bot detection with:

- Random requests delay
- Random fake agents each request