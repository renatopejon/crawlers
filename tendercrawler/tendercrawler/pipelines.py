# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from datetime import datetime
from itemadapter import ItemAdapter


class TendercrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert dates
        date_keys = ['publish_date', 'purchase_before', 'closing_date', 'opening_date']
        for key in date_keys:
            value = adapter.get(key)
            value = value.replace(',', ' ')
            value = datetime.strptime(value, '%A %d %B %Y')
            value = value.strftime('%Y-%m-%d')
            adapter[key] = value

        # Convert currency values to float
        currency_keys = ['initial_bond', 'tender_fees']
        for key in currency_keys:
            value = adapter.get(key)
            value = value.replace('BD', '')
            value = float(value)
            adapter[key] = value


        # Convert bid_validity to int
        bid_validity = adapter.get('bid_validity')
        bid_validity = bid_validity.replace('days', '')
        adapter['bid_validity'] = int(bid_validity)


        return item


class SQLitePipeline:
    def __init__(self) -> None:
        self.con = sqlite3.connect('tender.db')
        self.cur = self.con.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tenders(
                number TEXT,
                subject TEXT,
                ref_number TEXT,
                description TEXT,
                issued_by TEXT,
                category TEXT,
                type TEXT,
                initial_bond REAL,
                bid_validity_days INTEGER,
                tender_fees REAL,
                contract_duration TEXT,
                alternate_bid_allowed TEXT,
                publish_date TEXT,
                purchase_before TEXT,
                closing_date TEXT,
                opening_date TEXT
            )
        """)

    
    def process_item(self, item, spider):
        self.cur.execute("select * from tenders where number = ?", (item['number'],))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Item already in database: %s" % item['number'])

        else:
            self.cur.execute("""
                INSERT INTO tenders (
                    number, 
                    subject, 
                    ref_number, 
                    description, 
                    issued_by, 
                    category, 
                    type, 
                    initial_bond, 
                    bid_validity_days, 
                    tender_fees,
                    contract_duration,
                    alternate_bid_allowed,
                    publish_date,
                    purchase_before,
                    closing_date,
                    opening_date
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                item['number'],
                item['subject'],
                item['ref_number'],
                item['description'],
                item['issued_by'],
                item['category'],
                item['type'],
                item['initial_bond'],
                item['bid_validity'],
                item['tender_fees'],
                item['contract_duration'],
                item['alternate_bid_allowed'],
                item['publish_date'],
                item['purchase_before'],
                item['closing_date'],
                item['opening_date']
            ))

            self.con.commit()

        return item
