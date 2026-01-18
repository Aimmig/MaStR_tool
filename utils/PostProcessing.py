import pandas as pd
from utils.Constants import MANUFACTURERS
from utils.Helper import get_column_dict


class PostProcessing:
    @staticmethod
    def replace_manufacturer_str(val: str, manufacturer: tuple) -> str | None:
        """
        Helper function to return the new value for a manufacturer
        """
        old = manufacturer[0]
        new = manufacturer[1]
        if val is not None and old in val:
            return new
        else:
            return val

    @staticmethod
    def format_power(df: pd.DataFrame, unit: str) -> pd.DataFrame:
        """
        Formats the power value based on the given unit
        """
        power = "Nettonennleistung"
        if power not in df.columns.values:
            return df
        if unit == "kW":
            print("[INFO] Formating power to kW")
            df[power] = df[power].astype(int).astype(str) + " " + unit
        if unit == "MW":
            print("[INFO] Formating power MW")
            df[power] = df[power].div(1000).astype(str) + " " + unit
        return df

    @staticmethod
    def format_lambda(df: pd.DataFrame, column: str, manufacturer: tuple):
        """
        Helper method to apply the replacment of manufacturer names on one
        manufacturer
        """
        df[column] = df[column].apply(
                lambda x: PostProcessing.replace_manufacturer_str(
                    x, manufacturer)
                )
        return df

    @staticmethod
    def format_manufacturer(df: pd.DataFrame,
                            manufacturer_col: str) -> pd.DataFrame:
        """
        Applies the function for shortening/replacing manufacturer names to all
        """
        if manufacturer_col not in df.columns.values:
            return df
        for m in MANUFACTURERS.items():
            df = PostProcessing.format_lambda(df, manufacturer_col, m)
        return df

    @staticmethod
    def translate(df: pd.DataFrame, keep_columns: list[str]) -> pd.DataFrame:
        """
        Get all the columns and renames it with the dict,
        thereby translating it.
        Also throws away columns which should not be kept
        """
        # generate full dict and then only keep existing ones
        all_cols = get_column_dict(keep_columns, with_geometry=True)
        cols = {k: all_cols[k] for k in all_cols.keys() if k in df.columns.values}
        return df[cols.keys()].rename(columns=cols)
