import requests

def get_pages_count():
        url = "https://www.tenderboard.gov.bh/Templates/TenderBoardWebService.aspx/GetCurrentPublicTenderPageCount"
        payload = {
            "tenderNumber": "",
            "ministry": "0",
            "category": "0",
            "closingDate_filter": "",
            "publicTenderOnly": "true",
            "prequalificationOnly": "false",
            "auctionOnly": "true",
            "sortingType": "0",
            "listPage": "mainList",
            "Page": "1"
        }
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://www.tenderboard.gov.bh",
            "priority": "u=1, i",
            "referer": "https://www.tenderboard.gov.bh/Tenders/Public%20Tenders/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        dict = response.json()

        return dict['d']