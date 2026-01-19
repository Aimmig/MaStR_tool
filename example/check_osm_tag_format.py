from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getPlantsWithinArea
from utils.Helper import plot
import datetime
import pandas as pd


def check_power_value(osm: pd.DataFrame,
                      check_col: str) -> (pd.DataFrame, list[str]):
    known_good = "small_installation|MW|kW|yes"
    unusual = osm[~osm[check_col].str.contains(known_good, na=False)].dropna(subset=[check_col])
    print_cols = ['id'] + [check_col]
    return unusual, print_cols


def check_start_date(osm: pd.DataFrame,
                     check_col: str) -> (pd.DataFrame, list[str]):
    unusual = osm[osm[check_col].astype(str).str.contains(r'[0-9-]', regex=True)]
    print_cols = ['id'] + [check_col]
    return unusual, print_cols


def check_meter_values(osm: pd.DataFrame,
                       test_col: str) -> (pd.DataFrame, list[str]):
    unusual = osm[~osm[test_col].astype(str).str.isdigit()].dropna(subset=[test_col])
    unusual = unusual[unusual[test_col].astype(str).str.contains(' |,|m|"')]
    print_cols = ['id'] + ["height:hub", "rotor:diameter"]
    return unusual, print_cols


if __name__ == "__main__":
    parser = createOSMFormatParser()
    arguments = parser.parse_args()
    output = arguments.output
    osm_pbf = arguments.source
    check_col = arguments.tag
    osm_units = getPlantsWithinArea(osm_pbf)
    if check_col == "generator:output:electricity":
        filtered, cols = check_power_value(osm_units, check_col)
    if check_col == "height:hub":
        filtered, cols = check_meter_values(osm_units, check_col)
    if check_col == "rotor:diameter":
        filtered, cols = check_meter_values(osm_units, check_col)
    if check_col == "start_date":
        filtered, cols = check_date(osm_units, check_col)
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
    plot(check_col, cols, filtered)
