from utils.Constants import MANUFACTURERS
from utils.Constants import ROTOR, HUB
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
    Get part of df where tags like name/ref/description etc.
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
        ref_res = osm[(osm[col].str.len() == 33) &
                      (osm[col].str.startswith('E'))]
        res = pd.concat([res, ref_res])
    return res, ['id'] + [col]
