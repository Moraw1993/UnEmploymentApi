#############################################################
## Plik przetrzymujący dane do pobieranie informacji z API ##
#############################################################


## import packages
import logging
import os
import requests
import time


class Extractor:
    """
    Class for fetching data from an API.

    Methods:
        get_variable_id(): Retrieves the variable ID for a given month.
        fetch_data(): Fetches data from the API for a specific variable and year.
        get_next_page(): Retrieves the URL for the next page of results.

    Raises:
        ValueError: If an invalid month is provided.
        requests.exceptions.RequestException: If there is a problem with the internet connection.
    """

    def __init__(self):
        """
        Initializes the Api instance.
        """
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
        self.header_builder = HeaderBuilder(os.getenv("X-ClientId", None))

    def get_variable_id(self, month):
        """
        Retrieves the variable ID for a given month.

        Args:
            month: The month for which the variable ID is requested.

        Returns:
            str: The variable ID for the specified month.

        Raises:
            ValueError: If the provided month is invalid.
        """
        month_str = str(month)
        if month_str not in self.VARIABLE_ID_MAP.keys():
            raise ValueError("Invalid month")
        return self.VARIABLE_ID_MAP[month_str]

    def fetch_data(self, variable_id: str, year: str):
        """
        Fetches data from the API for a specific variable and year.

        Args:
            variable_id (str): The variable ID for which the data is to be fetched.
            year (str): The year for which the data is to be fetched.

        Returns:
            list: A list of dictionaries containing the fetched data.

        Raises:
            requests.exceptions.RequestException: If there is a problem with the internet connection.
        """
        stopa = []
        url = f"https://bdl.stat.gov.pl/api/v1/data/by-Variable/{variable_id}?year={year}&format=json&page-size=100"
        header = self.header_builder.build_header()
        starttime = time.time()
        while url:
            try:
                self.logger.info(f"Start trying to download data from the URL: {url}")
                response = self.request_handler.get(url, header)
            except requests.exceptions.RequestException:
                self.logger.error(
                    f"Problem with the internet connection:\n", exc_info=1
                )
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
                    try:
                        if row["id"] and len(row["id"]) == 12:
                            data_row = {
                                "id": row["id"],
                                "name": row["name"],
                                "stopa": row["values"][0]["val"],
                            }
                            stopa.append(data_row)
                        else:
                            raise ValueError(
                                "Id can't be None and should have 12 chars"
                            )
                    except:
                        logging.error(
                            "Something problem with ID column during extract data",
                            exc_info=1,
                        )
                        raise

                self.logger.info("Download completed successfully")
            else:
                return None

            endtime = time.time()
            if (endtime - starttime) < 0.1:
                time.sleep(0.1)

        return stopa

    def get_next_page(self, json: requests.Response):
        """
        Retrieves the URL for the next page of results.

        Args:
            json (requests.Response): The JSON response object.

        Returns:
            str: The URL for the next page of results, or None if there is no next page.
        """
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
        header = {
            "Host": "bdl.stat.gov.pl",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }
        if self.token:
            header["X-ClientId"] = self.token

        return header
