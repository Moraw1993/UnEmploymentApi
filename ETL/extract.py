#############################################################
## Plik przetrzymujący dane do pobieranie informacji z API ##
#############################################################


## import packages
import logging
import os
import requests
import time


class Api:
    def __init__(self):
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
        self.request_handler = RequestHandler()
        self.header_builder = HeaderBuilder(os.getenv("X-Client-Id"))

    def get_variable_id(self, month):
        month_str = str(month)
        if month_str not in self.VARIABLE_ID_MAP.keys():
            raise ValueError("Invalid month")
        return self.VARIABLE_ID_MAP[month_str]

    def fetch_data(self, variable_id: str, year: str):
        stopa = []
        url = f"https://bdl.stat.gov.pl/api/v1/data/by-Variable/{variable_id}?year={year}&format=json&page-size=100"
        header = self.header_builder.build_header()
        starttime = time.time()
        while url:
            try:
                self.logger.info(f"Start trying to download data from the URL: {url}")
                response = self.request_handler.get(url, header)
            except requests.exceptions.RequestException:
                self.logger.exception(f"Problem with the internet connection:\n")
                self.logger.info(
                    "No internet connection. Pausing data fetching. Will trying again at 30 sec"
                )
                time.sleep(30)
                if time.time() - starttime > 180:
                    self.logger.critical(
                        "after 3 minutes of reconnection attempts, the program ended",
                        stack_info=True,
                    )
                    raise requests.exceptions.RequestException
                continue
            except Exception as e:
                self.logger.exception("Other exception while get data")

            if self.request_handler.validate_response(response):
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

                self.logger.info("Download completed successfully")
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


class RequestHandler:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, header):
        return self.session.get(url=url, headers=header)

    def validate_response(self, response: requests.Response):
        if response.status_code != 200:
            response.raise_for_status()
        elif not response.json().get("results"):
            return False
        else:
            return True

    def check_internet_connection(self):
        try:
            requests.get("http://www.google.com", timeout=1)
            return True
        except requests.exceptions.RequestException:
            return False


class HeaderBuilder:
    def __init__(self, token):
        self.token = token

    def build_header(self):
        return {"Host": "bdl.stat.gov.pl", "X-ClientId": self.token}
