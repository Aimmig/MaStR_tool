import pandas as pd
from utils.Constants import MANUFACTURERS, COMMON_COLS, SELECT_COLS
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
    def createColumnDict(args) -> dict:
        cols = COMMON_COLS
        if args.keepColumns:
            colsToKeep = {k: SELECT_COLS[k] for k in args.keepColumns}
            cols.update(colsToKeep)
        return cols

    @staticmethod
    def printData(args, data: pd.DataFrame) -> None:
        # check subset before printing to avoid crash
        # when selecting non existing values
        cols = PostProcessing.createColumnDict(args)
        translatedHeader = True
        if args.translate:
            translatedHeader = list(cols.values())
        csv = data.to_csv(
                args.output,
                header=translatedHeader,
                columns=list(cols.keys()),
                index=False,
                )
        if csv:
            print(csv)
