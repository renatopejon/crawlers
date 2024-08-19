# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TendercrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TenderItem(scrapy.Item):
    number = scrapy.Field()
    subject = scrapy.Field()
    ref_number = scrapy.Field()
    description = scrapy.Field()
    issued_by = scrapy.Field()
    category = scrapy.Field()
    type = scrapy.Field()
    initial_bond = scrapy.Field()
    bid_validity = scrapy.Field()
    tender_fees = scrapy.Field()
    contract_duration = scrapy.Field()
    alternate_bid_allowed = scrapy.Field()
    publish_date = scrapy.Field()
    purchase_before = scrapy.Field()
    closing_date = scrapy.Field()
    opening_date = scrapy.Field()
