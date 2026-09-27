from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from dotenv import load_dotenv
from get_mastr_data_by_ref import get_data
from utils.Constants import REF_MASTR
from utils.Constants import CONSTRUCTION_POWER, PLANNED_POWER
from io import StringIO
import pandas as pd

DESC_CONSTR = "under construction"
GEN = "generator"
DESC = "description"


def fix_refs(refs):
    return [r for r in refs if len(r) == 15 and r.startswith("SEE")]


def filter_construction_or_planned(df):
    col_set = set(df.columns)
    if {CONSTRUCTION_POWER, PLANNED_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (DESC_CONSTR in df[DESC]) | (df[PLANNED_POWER] == GEN)]
    if {CONSTRUCTION_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (DESC_CONSTR in df[DESC])]
    if {CONSTRUCTION_POWER} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN)]


def get_construction_refs_osm(df):
    tags = filter_construction_or_planned(df)
    return tags[REF_MASTR].dropna().to_list()


def get_active_refs_osm(df):
    tags = df.loc[(df["power"] == GEN)]
    return tags[REF_MASTR].dropna().to_list()


def get_and_read_mastr(refs, cols):
    fixed_refs = fix_refs(refs)
    return pd.read_table(StringIO(get_data("wind", fixed_refs, cols)), sep=',')


def get_osm_potentially_open(area):
    osm_units = getWindPlantsInArea(area, sanitize=True)
    cols = ["Inbetriebnahmedatum", "Laengengrad", "Breitengrad"]
    constr_refs = get_construction_refs_osm(osm_units)
    maybe_open = get_and_read_mastr(constr_refs, cols)
    return maybe_open.dropna(subset=["Inbetriebnahmedatum"])


def get_osm_potentially_closed(area):
    osm_units = getWindPlantsInArea(area, sanitize=True)
    cols = ["DatumEndgueltigeStilllegung", "Laengengrad", "Breitengrad"]
    active_refs = get_active_refs_osm(osm_units)
    active = get_and_read_mastr(active_refs, cols)
    return active.dropna(subset=["DatumEndgueltigeStilllegung"])


def get_by_life_cyle(life_cyle: str, area: str):
    if life_cycle == "construction":
        return get_osm_potentially_open(area)
    if life_cycle == "disused":
        return get_osm_potentially_closed(area)


if __name__ == "__main__":
    env_file = "env_conf/.check_osm_life_cycle_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    #life_cycle = "construction"
    life_cycle = "disused"
    print(get_by_life_cyle(life_cycle, args.area))
