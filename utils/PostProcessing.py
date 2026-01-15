import pandas as pd
from utils.Constants import MANUFACTURERS, COMMON_COLS, SELECT_COLS, GEOMETRY_COLS
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
    def format_power(df: pd.DataFrame, unit: str) -> pd.DataFrame:
        power = "InstallierteLeistung"
        if power not in df.columns.values:
            return df
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
        if "Hersteller" not in df.columns.values:
            return df
        for m in MANUFACTURERS.items():
            df = PostProcessing.format_lambda(df, "Hersteller", m)
        return df

    @staticmethod
    def createColumnDict(args, withGeometry: bool) -> dict:
        cols = dict(COMMON_COLS)
        if withGeometry:
            cols.update(GEOMETRY_COLS)
        if args.keepColumns:
            colsToKeep = {k: SELECT_COLS[k] for k in args.keepColumns}
            cols.update(colsToKeep)
        return cols

    @staticmethod
    def translate(data: pd.DataFrame, args) -> pd.DataFrame:
        # generate full dict and then only keep existing ones
        allCols = PostProcessing.createColumnDict(args, withGeometry=True)
        cols = {k: allCols[k] for k in allCols.keys() if k in data.columns.values}
        return data[cols.keys()].rename(columns=cols)
