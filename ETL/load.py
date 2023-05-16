####################################
## Class to load data to csv file ##
####################################

import pandas as pd
import logging
import os
import threading


class FileManager:
    def __init__(self, output_folder=os.getenv("outputFolder", "output")):
        self.output_folder = output_folder

    def create_directory(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def get_file_path(self, file_name):
        return os.path.join(self.output_folder, file_name)

    def file_exists(self, file_path):
        return os.path.exists(file_path)

    def delete_file(self, file_path):
        os.remove(file_path)

    def create_file_name(self, month, year):
        return f"stopa powiaty {month}.{str(year)[2:]}.csv"


class CsvSaver:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.logger = logging.getLogger("__main__")

    def save_dataframe(self, dataframe: pd.DataFrame, month: str, year: str):
        if dataframe.empty:
            self.logger.warning("Dataframe is empty. File not saved.")
            return

        self.file_manager.create_directory()

        file_name = self.file_manager.create_file_name(month, year)
        file_path = self.file_manager.get_file_path(file_name)

        should_override = None

        def wait_for_input():
            nonlocal should_override
            should_override = input(
                f"File '{file_path}' already exists\n You have to 60 sec on a decision.\nDo you want to override it? (Y/N):\n"
            )

        if self.file_manager.file_exists(file_path):
            input_thread = threading.Thread(target=wait_for_input)
            input_thread.daemon = True
            input_thread.start()
            input_thread.join(timeout=60)

            if input_thread.is_alive():
                should_override = "Y"
                input_thread.join(timeout=1)

            if should_override.lower() != "y":
                self.logger.warning(
                    "File not saved cause you don't want overwrite existing file."
                )
                return
            else:
                self.file_manager.delete_file(file_path)
                self.logger.warning(
                    f"an existing file in the path: {file_path} has been deleted"
                )

        dataframe.to_csv(file_path, sep=";", index=False)
        self.logger.info(f"Dataframe saved successfully to '{file_path}'.")
