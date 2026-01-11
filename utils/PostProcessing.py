import pandas as pd
from utils.Constants import MANUFACTURERS


def replace_manufacturer_str(val: str, manufacturer: tuple):
    old = manufacturer[0]
    new = manufacturer[1]
    if val is not None and old in val:
        return new
    else:
        return val


def format_power(df: pd.DataFrame, unit: str):
    power = "InstallierteLeistung"
    if unit == "kW":
        df[power] = df[power].astype(int).astype(str) + " " + unit
    if unit == "MW":
        df[power] = df[power].div(1000).astype(str) + " " + unit
    return df


def format_lambda(df, column: str, manufacturer: tuple):
    df[column] = df[column].apply(
            lambda x: replace_manufacturer_str(x, manufacturer)
            )
    return df


def format_manufacturer(df: pd.DataFrame):
    for m in MANUFACTURERS.items():
        df = format_lambda(df, "Hersteller", m)
    return df
