from ETL.extract import Api
from ETL.transform import Transform
from ETL.load import FileManager, CsvSaver
from utilities import ConfigManager
import json
from logging import getLogger


class UnemploymentDownloader:
    def __init__(self, config=None, year=None, month=None) -> None:
        """
        Initialize the UnemploymentDownloader class.

        Args:
            config (str): Path to the configuration file (optional).
            year (str): Year to extract data for (optional).
            month (str): Month to extract data for (optional).
        """
        self.config = config
        self.year = year
        self.month = month
        self.stopy_bezrobocia = {}
        self.api = Api()
        self.transform = Transform()
        self.saver = CsvSaver(file_manager=FileManager())
        self.configManager = ConfigManager()
        self.logger = getLogger()

    def run_ETL(self):
        """
        Perform the ETL process - Extract, Transform, and Load.

        This method fetches data from an API, transforms it, and saves it to a CSV file.
        """
        key_dict = self.GetDictYearMonthToDownload()
        for year, month_list in key_dict.items():
            self.stopy_bezrobocia[year] = {}
            for month in month_list:
                variable_id = self.api.get_variable_id(month)
                data = self.api.fetch_data(variable_id, year)
                if not data:
                    self.logger.warning(
                        f"No data for variable: {variable_id}, year: {year}, month: {month}\n"
                        "The next data won't be downloaded.\n"
                        "The program is stopped."
                    )
                    break
                clear_data = self.transform.transform_data_from_API(data)
                self.stopy_bezrobocia[year][month] = clear_data
                self.saver.save_dataframe(clear_data, month, year)
                if self.config:
                    self.configManager.update_config("config.json", year, month, True)

    def GetDictYearMonthToDownload(self):
        """
        Determine the years and months for which data should be downloaded.

        Returns:
            dict: A dictionary with years as keys and corresponding month lists as values.
        """
        if self.config:
            try:
                self.configManager.load_config(self.config)
            except Exception as e:
                self.logger.exception(
                    "Error while trying read confing.json", stack_info=True
                )
            key_dict = self.configManager.get_download_options()
        else:
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

        self.logger.info(
            f"data for the following years and months will be downloaded:\n {json.dumps(key_dict, indent=4)}"
        )
        if not key_dict:
            self.logger.error("Empty key_dict")
        return key_dict
