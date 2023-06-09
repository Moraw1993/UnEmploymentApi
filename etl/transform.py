import pandas as pd
from typing import Dict
import re


class Transform:
    """
    Class for data transformation.

    Methods:
        transform_data_from_API(): Transforms data received from an API.
        filter_ID(): Filters DataFrame rows based on ID patterns.
        map_columns(): Reindexes columns and sorts values.
        transform_column(): Transforms values in a specific column.

    """

    def __init__(self):
        """
        Initializes the Transform instance.
        """
        pass

    def transform_data_from_API(self, data):
        """
        Transforms data received from an API.

        Args:
            data: Data received from the API.

        Returns:
            pd.DataFrame: Transformed DataFrame.

        """
        id_reg_pattern = {
            "Makro": r"^0([1-7])0{10}$",
            "Region": r"^0([1-7]\d{2}[1-2])0{7}$",
            "Podregion": r"0[1-7]\d{3}([0-9][1-9]|[1-9][0-9])0{5}$",
            "Nieokreślona": r"([0-9]{9}998)$",
            "Tekst": r".*REGION.*",
        }

        df = pd.DataFrame(data)
        df = df[df["id"].notnull()]

        df = self.filter_ID(df, id_reg_pattern)

        ## CREATE NEW COLUMNS
        df["WOJ."] = df["id"].str[2:4]
        df["POW."] = df["id"].str[7:9]
        df[""] = ""

        ## Reindex columns and sort values by woj and pow
        new_columns = ["WOJ.", "POW.", "", "name", "stopa"]
        df = self.map_columns(df, new_columns)

        ## Replace values in columns:
        df = self.transform_column(df, "name", "Powiat", "", False)
        df = self.transform_column(df, "stopa", ".", ",", False)

        ### Adds the prefix "WOJ." to name for all WOJ IDs.
        for index, row in df.iterrows():
            if row["WOJ."] != "00" and row["POW."] == "00":
                df.at[index, "name"] = "WOJ. " + row["name"]
        return df

    def filter_ID(self, df: pd.DataFrame, reg_pattern: Dict):
        """
        Filters DataFrame rows based on ID patterns.

        Args:
            df (pd.DataFrame): Input DataFrame.
            reg_pattern (Dict): Dictionary of ID patterns.

        Returns:
            pd.DataFrame: Filtered DataFrame.

        """
        for pat in reg_pattern.values():
            if pat == ".*REGION.*":
                df = df[
                    ~df["id"]
                    .astype(str)
                    .str.contains(pat, flags=re.IGNORECASE, regex=True)
                ]
            else:
                df = df[df["id"].astype("string").str.extract(pat, expand=False).isna()]
        return df

    def map_columns(self, df, new_columns):
        """
        Reindexes columns and sorts values.

        Args:
            df: Input DataFrame.
            new_columns: List of new column names.

        Returns:
            pd.DataFrame: Transformed DataFrame.

        """
        df = df.reindex(columns=new_columns)
        df.sort_values(by=["WOJ.", "POW."], inplace=True)
        df = df.reset_index(drop=True)
        return df

    def transform_column(
        self, df: pd.DataFrame, column: str, old_value: str, new_value: str, regex=True
    ):
        """
        Transforms values in a specific column.

        Args:
            df (pd.DataFrame): Input DataFrame.
            column (str): Name of the column to transform.
            old_value (str): Old value to replace.
            new_value (str): New value to assign.
            regex (bool, optional): Indicates if the transformation is regex-based. Defaults to True.

        Returns:
            pd.DataFrame: Transformed DataFrame.

        """
        df[column] = (
            df[column]
            .astype("string")
            .str.replace(old_value, new_value, regex=regex)
            .str.strip()
        )
        return df
