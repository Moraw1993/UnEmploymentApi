####################################
## Class to load data to csv file ##
####################################

import pandas as pd
import logging
import os
import threading


class FileManager:
    """
    Class for file management operations.

    Args:
        output_folder (str): Output folder path. Defaults to 'output' folder.

    Attributes:
        output_folder (str): Output folder path.

    """

    def __init__(self, output_folder=os.getenv("outputFolder", "output")):
        self.output_folder = output_folder

    def create_directory(self):
        """
        Creates the output directory if it doesn't exist.

        """

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def get_file_path(self, file_name):
        """
        Returns the full file path based on the output folder and the provided file name.

        Args:
            file_name (str): File name.

        Returns:
            str: Full file path.

        """

        return os.path.join(self.output_folder, file_name)

    def file_exists(self, file_path):
        """
        Checks if a file exists at the given file path.

        Args:
            file_path (str): File path.

        Returns:
            bool: True if the file exists, False otherwise.

        """

        return os.path.exists(file_path)

    def delete_file(self, file_path):
        """
        Deletes the file at the given file path.

        Args:
            file_path (str): File path.

        """

        os.remove(file_path)

    def create_file_name(self, month, year):
        """
        Creates a file name based on the month and year.

        Args:
            month (str): Month.
            year (str): Year.

        Returns:
            str: File name.

        """

        return f"stopa powiaty {month}.{str(year)[2:]}.csv"


class CsvSaver:
    """
    Class for saving a DataFrame as a CSV file.

    Args:
        file_manager (FileManager): Instance of FileManager for file management.

    Attributes:
        file_manager (FileManager): Instance of FileManager for file management.
        logger (logging.Logger): Logger instance.

    """

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.logger = logging.getLogger("__main__")

    def save_dataframe(self, dataframe: pd.DataFrame, month: str, year: str):
        """
        Saves a DataFrame as a CSV file.

        Args:
            dataframe (pd.DataFrame): DataFrame to be saved.
            month (str): Month for generate the name.
            year (str): Year for generate the name.

        """

        if dataframe.empty:
            self.logger.warning("Dataframe is empty. File not saved.")
            return

        # Create the output directory if it doesn't exist
        self.file_manager.create_directory()

        # Generate the file name based on the month and year
        file_name = self.file_manager.create_file_name(month, year)

        # Get the full file path
        file_path = self.file_manager.get_file_path(file_name)

        should_override = None

        def wait_for_input():
            nonlocal should_override
            should_override = input(
                f"File '{file_path}' already exists\nYou have 60 seconds to make a decision.\nDo you want to override it? (Y/N):\n"
            )

        if self.file_manager.file_exists(file_path):
            # If the file already exists, prompt the user for a decision within 60 seconds
            input_thread = threading.Thread(target=wait_for_input)
            input_thread.daemon = True
            input_thread.start()
            input_thread.join(timeout=60)

            if input_thread.is_alive():
                # If the user doesn't provide input within 60 seconds, assume "Y" (yes)
                should_override = "Y"
                input_thread.join(timeout=1)

            if should_override.lower() != "y":
                # If the user chose not to override the existing file, log a warning and return
                self.logger.warning(
                    "File not saved because you chose not to overwrite the existing file."
                )
                return
            else:
                # If the user chose to override, delete the existing file
                self.file_manager.delete_file(file_path)
                self.logger.warning(
                    f"An existing file at the path '{file_path}' has been deleted."
                )

        # Save the DataFrame as a CSV file
        dataframe.to_csv(file_path, sep=";", index=False, encoding="ANSI")
        self.logger.info(f"Dataframe saved successfully to the path: '{file_path}'.")
