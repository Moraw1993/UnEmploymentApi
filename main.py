############## IMPORT PACKAGES ##################
import argparse
import json
from ETL.extract import Api


class UnemploymentDownloader:
    def __init__(self, config=None, year=None, month=None) -> None:
        self.config = config
        self.year = year
        self.month = month
        self.stopy_bezrobocia = {}
        self.api = Api()
        self.tranform = None  ## ToDo
        self.saver = None  ## ToDo

    def extract_data(self):
        if self.config:
            with open(self.config) as config_file:
                config_data = json.load(config_file)
            key_dict = self.get_download_options(config_data)
        else:
            years = [self.year]
            months = [self.month]

        for year, month_list in key_dict.items():
            self.stopy_bezrobocia[year] = {}
            for month in month_list:
                variable_id = self.api.get_variable_id(month)
                data = self.api.fetch_data(variable_id, year)
                self.stopy_bezrobocia[year][month] = data  ## temporary
                # clear_data = self.transform.transform_data(data)
                # self.stopy_bezrobocia[year][month] = clear_data
                # self.saver.save_data(clear_data, month, year)
        print(self.stopy_bezrobocia)

    def get_download_options(self, config):
        key_to_download = {}
        for year, year_data in config["Year"].items():
            if not year_data["All_downloaded"]:
                key_to_download[year] = []
                for month, month_downloaded in year_data["Months"].items():
                    if not month_downloaded:
                        key_to_download[year].append(month)

        return key_to_download


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Extraction")
    parser.add_argument("--year", type=int, help="Year to extract data")
    parser.add_argument("--month", type=int, help="Month to extract data")
    parser.add_argument("--config", help="Configuration file path")

    args = parser.parse_args()

    if args.config:
        extractor = UnemploymentDownloader(config=args.config)
    elif args.year and args.month:
        extractor = UnemploymentDownloader(year=args.year, month=args.month)
    else:
        parser.error("Please provide either a config file or year and month.")

    extractor.extract_data()
