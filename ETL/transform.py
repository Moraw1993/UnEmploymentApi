import pandas as pd
from typing import Dict


class Transform:
    def __init__(self):
        pass

    def transform_data_for_API(self, data):
        id_reg_pattern = {
            "Makro": r"^0([1-7])0{10}$",
            "Region": r"^0([1-7]\d{2}[1-2])0{7}$",
            "Podregion": r"0[1-7]\d{3}([0-9][1-9]|[1-9][0-9])0{5}$",
            "Nieokreślona": r"([0-9]{9}998)$",
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
        # df["name"] = df["name"].str.replace("Powiat", "")
        # df["stopa"] = df["stopa"].astype("string").str.replace(".", ",", regex=False)

        ### Add string "WOJ." to name for all woj IDs
        for index, row in df.iterrows():
            if row["WOJ."] != "00" and row["POW."] == "00":
                df.at[index, "name"] = "WOJ. " + row["name"]
        return df

    def filter_ID(self, df: pd.DataFrame, reg_pattern: Dict):
        for pat in reg_pattern.values():
            df = df[df["id"].astype("string").str.extract(pat, expand=False).isna()]
        return df

    def map_columns(self, df, new_columns):
        df = df.reindex(columns=new_columns)
        df.sort_values(by=["WOJ.", "POW."], inplace=True)
        df = df.reset_index(drop=True)
        return df

    def transform_column(self, df, column, old_value, new_value, regex=True):
        df[column] = (
            df[column].astype("string").str.replace(old_value, new_value, regex=regex)
        )
        return df
