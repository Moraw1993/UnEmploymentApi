#############################################################
## Plik przetrzymujący dane do pobieranie informacji z API ##
#############################################################


## import packages
import logging
import os
import requests
import time


class Api:
    def __init__(self) -> None:
        self.ApiHelper = ApiHelper()
        self.VARIABLE_ID_MAP = {
            "01": "461680",
            "02": "461681",
            "03": "461682",
            "04": "461683",
            "05": "461684",
            "06": "461685",
            "07": "461686",
            "08": "461687",
            "09": "461688",
            "10": "461689",
            "11": "461690",
            "12": "461691",
        }
        self.logger = logging.getLogger("__main__")

    def get_variable_id(self, month):
        month_str = str(month)
        if month_str not in self.VARIABLE_ID_MAP.keys():
            raise ValueError("Invalid month")
        return self.VARIABLE_ID_MAP[month_str]

    def fetch_data(self, variable_id: str, year: str):
        stopa = []

        url = f"https://bdl.stat.gov.pl/api/v1/data/by-Variable/{variable_id}?year={year}&format=json&page-size=100"
        header = self.ApiHelper.getHeader()
        while url:
            starttime = time.time()
            ## get data
            try:
                ## log
                self.logger.info(f"Start trying download data from the URL: {url}")
                response = requests.get(url=url, headers=header)
            except Exception as e:
                self.logger.exception(f"problem with the: {str(type(e).__name__)}\n")
                raise
            if self.ApiHelper.validate_response(response):
                json = response.json()
                url = self.get_next_page(json)

                results = json["results"]
                for row in results:
                    if row["id"]:
                        data_row = {
                            "id": row["id"],
                            "name": row["name"],
                            "stopa": row["values"][0]["val"],
                        }
                        stopa.append(data_row)
                ##log
                self.logger.info("download completed successfully")
            else:
                return None
            endtime = time.time()
            if (endtime - starttime) < 0.1:
                time.sleep(0.1)
        return stopa

    def get_next_page(self, json: requests.Response):
        next_page_url = json["links"].get("next")
        if next_page_url:
            url = next_page_url
        else:
            url = None
        return url


class ApiHelper:
    def __init__(self) -> None:
        self.token = os.getenv("X-Client-Id")

    def getHeader(self):
        return {"Host": "bdl.stat.gov.pl", "X-ClientId": self.token}

    def validate_response(self, response: requests.Response):
        if response.status_code != 200:
            response.raise_for_status()
        elif not response.json().get("results"):
            return False
        else:
            return True
