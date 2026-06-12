from utils.Constants import MANUFACTURERS
from utils.Constants import POWER, ROTOR, HUB, START, END
from utils.Constants import REF_MASTR, REF_EEG
from utils.Constants import OTHER_OSM
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
    col_raw = col + "_raw"
    res = osm[osm[col_raw].str.contains(r'[.\\/]', regex=True, na=False)]
    res[col] = res[col_raw]
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
    Get part of df where tags like name/ref/description etc.
    contains some things that potentially shouldn't be in these tags.
    """
    man_short = list(MANUFACTURERS.values())
    man_long = list(MANUFACTURERS.keys())
    words_lifecycle = ["WKA", "WEA", "abgebaut", "dismantled", "removed", "demolished",
                       "zurückgebaut", "im Bau", "geplant", "construction"]
    words_power = ["MW", "kW", "KW"]
    words_ref = ["MaStR", "EEG"]
    search_list = [*man_short, *man_long,
                   *words_lifecycle, *words_power, *words_ref]
    sep = "|"
    search = sep.join(search_list)
    if col != REF_MASTR:
        search = search + sep + "SEE"
    res = osm[osm[col].str.contains(search, na=False)]
    # Find where matches with Exxxxxx ref number exits and add those, too
    if col != REF_EEG:
        ref_res = osm[(osm[col].str.len() == 33) &
                      (osm[col].str.startswith('E'))]
        res = pd.concat([res, ref_res])
    return res, ['id'] + [col]


def get_non_empty(osm: pd.DataFrame,
                  col: str) -> (pd.DataFrame, list[str]):
    return osm.dropna(subset=[col]), ['id'] + [col]


def check_tags(osm_units: pd.DataFrame,
               check_col: str, strict=False) -> (pd.DataFrame, list[str]):
    if check_col in [POWER]:
        return check_power_value(osm_units, check_col)
    if check_col in [HUB, ROTOR]:
        return check_meter_values(osm_units, check_col)
    if check_col in [START, END]:
        return check_date(osm_units, check_col)
    if check_col in ["designation", "description", "note", "name"] and strict:
        return get_non_empty(osm_units, check_col)
    if check_col in OTHER_OSM + [REF_MASTR, REF_EEG]:
        return check_name(osm_units, check_col)
    return None, None
