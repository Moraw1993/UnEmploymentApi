############################################
## Classes to help manage the application ##
############################################

import json
from abc import ABC, abstractmethod


class IConfigManager(ABC):
    @abstractmethod
    def load_config(self, file_path: str) -> None:
        pass

    @abstractmethod
    def update_config(self, file_path: str, year: str, month: str, value: any) -> None:
        pass

    @abstractmethod
    def validate_config(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def get_value(self, key: str) -> any:
        pass


class ConfigManager(IConfigManager):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.config = {}

    def load_config(self, file_path: str) -> None:
        """
        Loads the configuration data from a file.

        Args:
            file_path (str): The path to the configuration file.
        """
        with open(file_path) as f:
            self.config = json.load(f)

    def update_config(
        self, file_path: str, year: str, month: str, value: bool = True
    ) -> None:
        """
        Updates the configuration for a specific year and month with the provided value.

        Args:
            file_path (str): The path to the configuration file.
            year (str): The year for which the configuration needs to be updated.
            month (str): The month for which the configuration needs to be updated.
            value (bool): The value to be set for the specified year and month.

        Raises:
            ValueError: If the specified year or month is invalid or not found in the config file.
        """
        year_config = self._get_year_config(year)

        month_config_parent = year_config["Months"]

        if month in month_config_parent:
            month_config_parent[month] = value
            year_config["All_downloaded"] = all(
                month_downloaded for month_downloaded in year_config["Months"].values()
            )
        else:
            raise ValueError(
                f"Invalid month '{month}'. Month not found for year '{year}' in config file."
            )

        with open(file_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_value(self, key: str) -> any:
        """
        Retrieves the value associated with the specified key from the configuration.

        Args:
            key (str): The key for which the value needs to be retrieved.

        Returns:
            any: The value associated with the specified key, or None if the key is not found.
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        return value

    def get_download_options(self):
        """
        Retrieves the years and months that have not been fully downloaded.

        Returns:
            dict: A dictionary containing the years as keys and the list of months to be downloaded as values.
        """
        key_to_download = {}
        for year, year_data in self.config["Year"].items():
            if not self.get_value(f"Year.{year}.All_downloaded"):
                key_to_download[year] = [
                    month
                    for month, downloaded in year_data["Months"].items()
                    if not downloaded
                ]
        return key_to_download

    def add_next_year(self, file_path: str) -> None:
        """
        Adds the next year to the configuration file.

        Args:
            file_path (str): The path to the configuration file.
        """
        # Check the earliest year
        years = self.config["Year"].keys()
        earliest_year = max(map(int, years))

        # Create the next year and months from 01 to 12
        next_year = str(earliest_year + 1)
        self.config["Year"][next_year] = {
            "All_downloaded": False,
            "Months": {str(month).zfill(2): False for month in range(1, 13)},
        }

        # Save the changes to the file
        with open(file_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def _validate_year_in_config(self):
        if "Year" not in self.config:
            raise ValueError("Invalid config file. 'Year' key not found.")

    def _get_year_config(self, year: str) -> str:
        """
        Retrieves the configuration for a specific year.

        Args:
            year (str): The year for which the configuration is requested.

        Returns:
            str: The configuration for the specified year.

        Raises:
            ValueError: If the specified year is invalid or not found in the config file.
        """
        self._validate_year_in_config()

        year_config = self.config["Year"].get(year)
        if year_config is None:
            raise ValueError(f"Invalid year '{year}'. Year not found in config file.")

        return year_config

    def _get_month_config(self, year_config: str, month: str) -> str:
        """Method get month value from dict for the specific year

        Args:
            year_config (str): The year for which you want to download the month
            month (str): The month for which you want to download value

        Raises:
            ValueError: If month not exist in year raise ValueError

        Returns:
            str: Month value of the year
        """
        month_config = year_config["Months"].get(month)
        if month_config is None:
            raise ValueError(
                f"Invalid month '{month}'. Month not found for year '{year_config}' in config file."
            )

        return month_config
