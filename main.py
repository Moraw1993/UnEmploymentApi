############## IMPORT PACKAGES ##################
import argparse
import json
import time
import logging
from ETL.extract import Api
from ETL.transform import Transform
from dotenv import load_dotenv


class UnemploymentDownloader:
    def __init__(self, config=None, year=None, month=None) -> None:
        self.config = config
        self.year = year
        self.month = month
        self.stopy_bezrobocia = {}
        self.api = Api()
        self.transform = Transform()  ## ToDo
        self.saver = None  ## ToDo

    def extract_data(self):
        if self.config:
            try:
                with open(self.config) as config_file:
                    config_data = json.load(config_file)
            except Exception as e:
                logger.exception("Error while trying read confing.json")
            key_dict = self.get_download_options(config_data)
        else:
            key_dict = {self.year: [self.month]}

        logger.info(
            f"data for the following years and months will be downloaded:\n {json.dumps(key_dict, indent=4)}"
        )
        for year, month_list in key_dict.items():
            self.stopy_bezrobocia[year] = {}
            for month in month_list:
                variable_id = self.api.get_variable_id(month)
                ## fetch data
                data = self.api.fetch_data(variable_id, year)
                if not data:
                    logger.warning(
                        f"No data for variable: {variable_id}, year: {year}, month: {month}\n"
                        "The next data won't be downloaded.\n"
                        "The program is stopped."
                    )
                    break
                # self.stopy_bezrobocia[year][month] = data  ## temporary
                clear_data = self.transform.transform_data_for_API(data)
                self.stopy_bezrobocia[year][month] = clear_data
                print(clear_data)
                # self.saver.save_data(clear_data, month, year)

        ##print(self.stopy_bezrobocia)

    def get_download_options(self, config):
        key_to_download = {}
        for year, year_data in config["Year"].items():
            if not year_data["All_downloaded"]:
                key_to_download[year] = []
                for month, month_downloaded in year_data["Months"].items():
                    if not month_downloaded:
                        key_to_download[year].append(month)
        return key_to_download


# Custom formatter
class MyFormatter(logging.Formatter):
    formats = {
        logging.DEBUG: "%(module)s: %(lineno)d: %(msg)s",
        logging.INFO: "%(asctime)s - %(levelname)s - %(message)s",
        logging.WARNING: "%(asctime)s - %(levelname)s - %(message)s",
        logging.ERROR: "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s",
    }

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        super().__init__(fmt)

    def format(self, record):
        # Get the format based on the logging level
        log_fmt = self.formats.get(record.levelno, self._fmt)

        # Call the original formatter class to do the grunt work
        result = logging.Formatter(log_fmt).format(record)

        return result


def initialize_logger():
    starttime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    logger = logging.getLogger(__name__)

    fmt = MyFormatter()

    hdlr = logging.FileHandler(f"Logs/{starttime}.log", mode="w")
    hdlr.setLevel(logging.INFO)
    hdlr.setFormatter(fmt)

    ch = logging.StreamHandler()  # Dodanie StreamHandlera dla logów konsolowych
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(hdlr)
    logger.addHandler(ch)  # Dodanie StreamHandlera do loggera

    logger.setLevel(logging.DEBUG)
    # logger.propagate = True  ## wyłącza logowanie w konsoli
    return logger


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Data Extraction")
    group = parser.add_argument_group("Get data for one Year/Month")
    group.description = "Example --year 2023 --month 05"
    group.add_argument(
        "--year", type=str, help="Year to extract data", required=False, nargs=1
    )
    group.add_argument(
        "--month", type=str, help="Month to extract data", required=False, nargs=1
    )
    ## Get data fron config.json
    parser.add_argument(
        "--config",
        help="Get data for years and months from the config.json",
        choices=["config.json"],
        default="config.json",
        nargs=1,
    )

    args = parser.parse_args()

    if args.config and (args.year or args.month):
        parser.error(
            "Please provide either a config file or year and month, but not both."
        )
    if args.config:
        extractor = UnemploymentDownloader(config=args.config)
    elif args.year and args.month:
        extractor = UnemploymentDownloader(year=args.year, month=args.month)
    else:
        parser.error("Please provide either a config file or year and month.")

    logger = initialize_logger()
    logger.info(f"Start program with the arguments: {args}")
    extractor.extract_data()
