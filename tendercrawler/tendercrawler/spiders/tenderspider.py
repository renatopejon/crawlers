import json
import scrapy
from tendercrawler.items import TenderItem

from .functions import get_pages_count


class TenderspiderSpider(scrapy.Spider):
    name = "tenderspider"
    start_page = 1
    end_page = get_pages_count()

    def start_requests(self):
        url = 'https://www.tenderboard.gov.bh/Templates/TenderBoardWebService.aspx/GetCurrentPublicTenderByPage'
        
        for page in range(self.start_page, self.end_page):
            body = {
                "tenderNumber": "",
                "ministry": "0",
                "category": "0",
                "closingDate_filter": "",
                "publicTenderOnly": "true",
                "prequalificationOnly": "false",
                "auctionOnly": "true",
                "sortingType": "0",
                "listPage": "mainList",
                "Page": str(page)
            }

            request_body = json.dumps(body)

            yield scrapy.Request(
                url=url,
                method='POST',
                body=request_body,
                callback=self.parse,
            )

    def parse(self, response):
        rows = response.jmespath('d').css('div.rows')

        for row in rows:
            columns = row.css('div.column')
            relative_url = columns[1].css('div a').attrib['href']
            tender_url = f"https://www.tenderboard.gov.bh/{relative_url}"

            yield response.follow(tender_url, callback= self.parse_tender_page)

    def parse_tender_page(self, response):
        tender = TenderItem(
            subject = response.css('div.case-detail-info h3::text').get(),
            number = response.css('p.case-cate span::text').getall()[0],
            ref_number = response.css('p.case-cate span::text').getall()[1],
            description = response.css('h4 + p::text').get(),
            issued_by = response.css('dl.dl-horizontal dd::text').getall()[0],
            category = response.css('dl.dl-horizontal dd::text').getall()[1],
            type = response.css('dl.dl-horizontal dd::text').getall()[2],
            initial_bond = response.css('dl.dl-horizontal dd::text').getall()[3],
            bid_validity = response.css('dl.dl-horizontal dd::text').getall()[4],
            tender_fees = response.css('dl.dl-horizontal dd::text').getall()[5],
            contract_duration = response.css('dl.dl-horizontal dd::text').getall()[6],
            alternate_bid_allowed = response.css('dl.dl-horizontal dd::text').getall()[7],
            publish_date = response.css('dl.dl-horizontal dd::text').getall()[8],
            purchase_before = response.css('dl.dl-horizontal dd::text').getall()[9],
            closing_date = response.css('dl.dl-horizontal dd span::text').get(),
            opening_date = response.css('dl.dl-horizontal dd::text').getall()[10],
        )
        
        yield tender


    # def parse(self, response):
    #     rows = response.jmespath('d').css('div.rows')
    #     for row in rows:
    #         columns = row.css('div.column')
    #         tender = TenderItem(
    #             number = columns[1].css('div a span::text').get(),
    #             subject = columns[1].css('div a::text').get(),
    #             relative_url = columns[1].css('div a').attrib['href'],
    #             type = columns[2].css('div::text').get(),
    #             category = columns[3].css('div::text').get(),
    #             purchasing_authority = columns[4].css('div::text').get(),
    #             purchase_before = columns[5].css('div span::text').get(),
    #             closing_date = columns[6].css('div span::text').get(),
    #         )
    #         yield tender
