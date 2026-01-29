from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getPlantsWithinArea
from utils.Helper import plot
from utils.Constants import MANUFACTURERS
from utils.Constants import POWER, ROTOR, HUB, START, END
from utils.Constants import REF_MASTR, REF_EEG
import pandas as pd


def check_power_value(osm: pd.DataFrame,
                      col: str) -> (pd.DataFrame, list[str]):
    """
    Get part of df where power tag is potentially malformed.
    """
    valid = "small_installation|MW|kW|yes"
    res = osm[~osm[col].str.contains(valid, na=False)].dropna(subset=[col])
    return res, ['id'] + [col]


def check_date(osm: pd.DataFrame,
               col: str) -> (pd.DataFrame, list[str]):
    """
    Get part of df where date contains something else than [0-9] and dash.
    """
    res = osm[osm[col].astype(str).str.contains(r'[0-9-]', regex=True)]
    return res, ['id'] + [col]


def check_meter_values(osm: pd.DataFrame,
                       col: str) -> (pd.DataFrame, list[str]):
    """
    Get part of df where length tags are potentially malformed.
    """
    res = osm[~osm[col].astype(str).str.isdigit()].dropna(subset=[col])
    res = res[res[col].astype(str).str.contains(' |,|m|"')]
    return res, ['id'] + [HUB, ROTOR]


def check_name(osm: pd.DataFrame,
               col: str) -> (pd.DataFrame, list[str]):
    """
    Get part of df where tags like name/ref/descripton ect..
    contains some things that potentially shouldn't be in these tags.
    """
    sep = "|"
    man_short = sep.join(MANUFACTURERS.values())
    man_long = sep.join(MANUFACTURERS.keys())
    search = 'MW|kW|KW|MaStR|EEG' + man_short + sep + man_long
    if col != REF_MASTR:
        search = search + sep + "SEE"
    res = osm[osm[col].str.contains(search, na=False)]
    # Find where matches with Exxxxxx ref number exits and add those, too
    if col != REF_EEG:
        ref_res = osm[(osm[col].str.len() == 33) & (osm[col].str.startswith('E'))]
        res = pd.concat([res, ref_res])
    return res, ['id'] + [col]


if __name__ == "__main__":
    parser = createOSMFormatParser()
    arguments = parser.parse_args()
    output = arguments.output
    osm_pbf = arguments.source
    check_col = arguments.tag
    gen_source = "wind"
    gen_method = "wind_turbine"
    osm_units = getPlantsWithinArea(osm_pbf, gen_source,
                                    gen_method, sanitize=False)
    filtered = None
    cols = None
    if check_col in [POWER]:
        filtered, cols = check_power_value(osm_units, check_col)
    if check_col in [HUB, ROTOR]:
        filtered, cols = check_meter_values(osm_units, check_col)
    if check_col in [START, END]:
        filtered, cols = check_date(osm_units, check_col)
    if check_col in ["name", "description", "note", "ref", REF_MASTR, REF_EEG]:
        filtered, cols = check_name(osm_units, check_col)
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
    plot(check_col, cols, filtered)
