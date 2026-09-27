from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from dotenv import load_dotenv
from get_mastr_data_by_ref import get_data
from utils.Constants import REF_MASTR
from utils.Constants import CONSTRUCTION_POWER, PLANNED_POWER
import pandas as pd

DESC_CONSTR = "under construction"
GEN = "generator"
DESC = "description"


def fix_refs(refs: list[str]):
    """
    Fixes the list of refs by dropping all elements
    which are unexpected in this context
    """
    return [r for r in refs if len(r) == 15 and r.startswith("SEE")]


def filter_construction_or_planned(df: pd.DataFrame):
    """
    Filter dataframe where units are considered
    as under construction/planned etc
    """
    col_set = set(df.columns)
    if {CONSTRUCTION_POWER, PLANNED_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (DESC_CONSTR in df[DESC]) | (df[PLANNED_POWER] == GEN)]
    if {CONSTRUCTION_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (DESC_CONSTR in df[DESC])]
    if {CONSTRUCTION_POWER} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN)]


def get_construction_refs_osm(df: pd.DataFrame):
    """
    Filters for units which are considered as
    tagged construction and ref:mastr exists
    """
    tags = filter_construction_or_planned(df)
    return tags[REF_MASTR].dropna().to_list()


def get_active_refs_osm(df: pd.DataFrame):
    """
    Filters for units which are considered operational
    and ref:mastr exists
    """
    tags = df.loc[(df["power"] == GEN)]
    return tags[REF_MASTR].dropna().to_list()


def get_and_read_mastr(refs: list[str], cols: list[str]):
    """
    Gets the MaStR data for the refs
    """
    fixed_refs = fix_refs(refs)
    return get_data("wind", fixed_refs, cols)


def get_osm_potentially_open(area: str):
    """
    Gets all osm wind units in area which are considered as
    tagged construction
    If possible gets MaStR-Data for these units.
    Returns units where construction has already finished.
    """
    osm_units = getWindPlantsInArea(area, sanitize=True)
    constr_refs = get_construction_refs_osm(osm_units)
    cols = ["Inbetriebnahmedatum", "Laengengrad", "Breitengrad"]
    maybe_open = get_and_read_mastr(constr_refs, cols)
    return maybe_open.dropna(subset=["Inbetriebnahmedatum"])


def get_osm_potentially_closed(area: str):
    """
    Gets all osm wind units in area which are considered as
    currently operational.
    If possible gets MaStR-Data for these units.
    Returns units which have been permanently shut down.
    """
    osm_units = getWindPlantsInArea(area, sanitize=True)
    active_refs = get_active_refs_osm(osm_units)
    cols = ["DatumEndgueltigeStilllegung", "Laengengrad", "Breitengrad"]
    active = get_and_read_mastr(active_refs, cols)
    return active.dropna(subset=["DatumEndgueltigeStilllegung"])


def get_by_life_cyle(life_cyle: str, area: str):
    """
    Get units for specified lifecyle
    """
    if life_cycle == "construction":
        return get_osm_potentially_open(area)
    if life_cycle == "disused":
        return get_osm_potentially_closed(area)


if __name__ == "__main__":
    env_file = "env_conf/.check_osm_life_cycle_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    life_cycle = "construction"
    # life_cycle = "disused"
    print(get_by_life_cyle(life_cycle, args.area))
