import pandas as pd
from utils.Constants import COMMON_COLS, SELECT_COLS, GEOMETRY_COLS
from utils.Constants import MANUFACTURERS


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
    def format_manufacturer(df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the function for shortening/replacing manufacturerer names
        to all Manufactueres
        """
        if "Hersteller" not in df.columns.values:
            return df
        for m in MANUFACTURERS.items():
            df = PostProcessing.format_lambda(df, "Hersteller", m)
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


def get_column_dict(keep_columns: list[str], with_geometry: bool) -> dict:
    """
    Creates the dict of all columns for translation.
    Always includes COMMON_COLS
    If specified includes the geometry column
    Includes all key-value pairs matching keep_column
    """
    cols = dict(COMMON_COLS)
    if with_geometry:
        cols.update(GEOMETRY_COLS)
    if keep_columns:
        cols_to_keep = {k: SELECT_COLS[k] for k in keep_columns}
        cols.update(cols_to_keep)
    return cols


def get_cols_without_geometry(keep_columns: list[str]) -> list[str]:
    """
    Wrapper method to get all translated (values) without the geometry column
    """
    return list(get_column_dict(keep_columns, with_geometry=False).values())


def check_cols_in_dataframe(df: pd.DataFrame, columns: list[str]) -> list[str]:
    """
    Checks the columns list against df
    Returns part of columns list that is present in df
    """
    existing = []
    for c in columns:
        if c in df.columns:
            existing.append(c)
        else:
            print("[INFO] " + c + " does not exist. Ignoring column")
    return existing


# TO-DO relax strict assumptions for later imports
def check_strict(df: pd.DataFrame, col: str) -> pd.DataFrame:
    mastr = "`" + col + "_mastr`"
    osm = "`" + col + "_osm`"
    return df.query(f"({osm} == {mastr})")
