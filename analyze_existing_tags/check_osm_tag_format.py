from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getPlantsWithinArea
from utils.Helper import plot
from utils.Constants import MANUFACTURERS
from utils.Constants import POWER, ROTOR, HUB, START, END
import pandas as pd


def check_power_value(osm: pd.DataFrame,
                      col: str) -> (pd.DataFrame, list[str]):
    valid = "small_installation|MW|kW|yes"
    res = osm[~osm[col].str.contains(valid, na=False)].dropna(subset=[col])
    return res, ['id'] + [col]


def check_date(osm: pd.DataFrame,
                     col: str) -> (pd.DataFrame, list[str]):
    res = osm[osm[col].astype(str).str.contains(r'[0-9-]', regex=True)]
    return res, ['id'] + [col]


def check_meter_values(osm: pd.DataFrame,
                       col: str) -> (pd.DataFrame, list[str]):
    res = osm[~osm[col].astype(str).str.isdigit()].dropna(subset=[col])
    res = res[res[col].astype(str).str.contains(' |,|m|"')]
    return res, ['id'] + [HUB, ROTOR]


def check_name(osm: pd.DataFrame,
               col: str) -> (pd.DataFrame, list[str]):
    sep = "|"
    man_short = sep.join(MANUFACTURERS.values())
    man_long = sep.join(MANUFACTURERS.keys())
    search = 'MW|kW|KW|' + man_short + sep + man_long
    res = osm[osm[col].str.contains(search, na=False)]
    return res, ['id'] + [col]


if __name__ == "__main__":
    parser = createOSMFormatParser()
    arguments = parser.parse_args()
    output = arguments.output
    osm_pbf = arguments.source
    check_col = arguments.tag
    osm_units = getPlantsWithinArea(osm_pbf)
    filtered = None
    cols = None
    if check_col in [POWER]:
        filtered, cols = check_power_value(osm_units, check_col)
    if check_col in [HUB, ROTOR]:
        filtered, cols = check_meter_values(osm_units, check_col)
    if check_col in [START, END]:
        filtered, cols = check_date(osm_units, check_col)
    if check_col in ["name", "description", "note"]:
        filtered, cols = check_name(osm_units, check_col)
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
    plot(check_col, cols, filtered)
