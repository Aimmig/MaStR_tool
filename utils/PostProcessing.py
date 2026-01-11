import pandas as pd
from utils.Constants import MANUFACTURERS
from utils.DataFilter import DataFilter


class PostProcessing:
    @staticmethod
    def replace_manufacturer_str(val: str, manufacturer: tuple) -> str | None:
        old = manufacturer[0]
        new = manufacturer[1]
        if val is not None and old in val:
            return new
        else:
            return val

    @staticmethod
    # TO-DO make power variable parameter to work with different cases
    def format_power(df: pd.DataFrame, unit: str) -> pd.DataFrame:
        power = "InstallierteLeistung"
        if unit == "kW":
            df[power] = df[power].astype(int).astype(str) + " " + unit
        if unit == "MW":
            df[power] = df[power].div(1000).astype(str) + " " + unit
        return df

    @staticmethod
    def format_lambda(df: pd.DataFrame, column: str, manufacturer: tuple):
        df[column] = df[column].apply(
                lambda x: PostProcessing.replace_manufacturer_str(
                    x, manufacturer)
                )
        return df

    @staticmethod
    def format_manufacturer(df: pd.DataFrame) -> pd.DataFrame:
        for m in MANUFACTURERS.items():
            df = PostProcessing.format_lambda(df, "Hersteller", m)
        return df

    @staticmethod
    def get_renamed(df: pd.DataFrame, cols: dict) -> pd.DataFrame:
        return DataFilter.get_columns(df, cols).rename(cols, axis='columns')
