############################################
## Classes to help manage the application ##
############################################

# TODO Add the ConfigManager


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
        with open(file_path) as f:
            self.config = json.load(f)

    def update_config(self, file_path: str, year: str, month: str, value: bool) -> None:
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

    def validate_config(self, file_path: str) -> bool:
        try:
            with open(file_path) as f:
                json.load(f)
            return True
        except (ValueError, FileNotFoundError):
            return False

    def get_value(self, key: str) -> any:
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        return value

    def get_download_options(self):
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
        # Sprawdzenie najwcześniejszego roku
        years = self.config["Year"].keys()
        earliest_year = max(map(int, years))

        # Utworzenie kolejnego roku i miesięcy od 01 do 12
        next_year = str(earliest_year + 1)
        self.config["Year"][next_year] = {
            "All_downloaded": False,
            "Months": {str(month).zfill(2): False for month in range(1, 13)},
        }

        # Zapisanie zmian do pliku
        with open(file_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def _validate_config(self):
        if "Year" not in self.config:
            raise ValueError("Invalid config file. 'Year' key not found.")

    def _get_year_config(self, year):
        self._validate_config()

        year_config = self.config["Year"].get(year)
        if year_config is None:
            raise ValueError(f"Invalid year '{year}'. Year not found in config file.")

        return year_config

    def _get_month_config(self, year_config, month):
        month_config = year_config["Months"].get(month)
        if month_config is None:
            raise ValueError(
                f"Invalid month '{month}'. Month not found for year '{year_config}' in config file."
            )

        return month_config
