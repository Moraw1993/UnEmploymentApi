############## IMPORT PACKAGES ##################
import argparse
import json
import time
from logger import get_logger
from ETL.extract import Api
from ETL.transform import Transform
from ETL.load import FileManager, CsvSaver
from utilities import ConfigManager
from dotenv import load_dotenv


class UnemploymentDownloader:
    def __init__(self, config=None, year=None, month=None) -> None:
        self.config = config
        self.year = year
        self.month = month
        self.stopy_bezrobocia = {}
        self.api = Api()
        self.transform = Transform()  ## ToDo
        self.saver = CsvSaver(file_manager=FileManager())  ## ToDo
        self.configManager = ConfigManager()

    def extract_data(self):
        if self.config:
            try:
                self.configManager.load_config(self.config)
            except Exception as e:
                logger.exception("Error while trying read confing.json")
            key_dict = self.configManager.get_download_options()
        else:
            ## if only the year argument is set then set the month variable to all months of the year
            if self.month is None:
                self.month = [
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                ]
            if not isinstance(self.month, list):
                self.month = [self.month]
            key_dict = {self.year: self.month}

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
                self.saver.save_dataframe(clear_data, month, year)
                if self.config:
                    self.configManager.update_config("config.json", year, month, True)

        ##print(self.stopy_bezrobocia)


def validate_year(year):
    if len(year) != 4 or not year.isdigit():
        raise argparse.ArgumentTypeError("Year must have 4 digits.")
    year_int = int(year)
    if year_int < 2000 or year_int > 2099:
        raise argparse.ArgumentTypeError("Year must be in the range 2000-2099.")
    return year


def validate_month(month):
    if len(month) != 2 or not month.isdigit():
        raise argparse.ArgumentTypeError("Month must have 2 digits.")
    return month


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Data Extraction")
    group = parser.add_argument_group("Get data for one Year/Month")
    group.description = "Example: python main_script.py --year 2023 --month 05"
    group.add_argument(
        "--year",
        type=validate_year,
        help="Year from range (2000-2099) to extract data.\nThis argument can be used alone",
    )
    group.add_argument(
        "--month",
        type=validate_month,
        help="Month to extract data.\nthis argument must be used with --year",
        choices=[
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
        ],
    )
    ## Get data fron config.json
    parser.add_argument(
        "--config",
        help="Get data for years and months from the config.json",
        choices=["config.json"],
    )
    parser.add_argument(
        "--add_year",
        help="Add the next year with all months set to False in the config.json",
        action="store_true",
    )
    ##TODO Add parser for add next year with false value to the config.json

    args = parser.parse_args()

    if args.config and (args.year or args.month or args.add_year):
        parser.error(
            "Please provide either a config file or year and month, but not both."
        )
    if args.config:
        extractor = UnemploymentDownloader(config=args.config)
    elif args.year or args.month:
        extractor = UnemploymentDownloader(year=args.year, month=args.month)
    elif args.add_year:
        config_manager = ConfigManager()
        config_manager.load_config("config.json")
        config_manager.add_next_year("config.json")
        exit()
    else:
        parser.error("Please provide either a config file or year and month.")

    logger = get_logger(__name__)
    logger.info(f"Start program with the arguments: {args}")
    extractor.extract_data()
    logger.info(f"The program has ended successfully.")
    exit()
