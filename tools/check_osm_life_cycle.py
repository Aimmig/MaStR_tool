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


def filter_construction_or_planned(df):
    col_set = set(df.columns)
    if {CONSTRUCTION_POWER, PLANNED_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (df[DESC] == DESC_CONSTR) | (df[PLANNED_POWER] == GEN)]
    if {CONSTRUCTION_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (df[DESC] == DESC_CONSTR)]
    if {CONSTRUCTION_POWER} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN)]


def get_construction_refs_osm(df):
    tags = filter_construction_or_planned(df)
    return tags[REF_MASTR].dropna().to_list()


def get_osm_potentially_open(area):
    osm_units = getWindPlantsInArea(area, sanitize=True)
    cols = ["Inbetriebnahmedatum", "Laengengrad", "Breitengrad"]
    constr_refs = get_construction_refs_osm(osm_units)
    maybe_open = pd.read_table(StringIO(get_data("wind", constr_refs, cols)), sep=',')
    return maybe_open.dropna(subset=["Inbetriebnahmedatum"])

if __name__ == "__main__":
    env_file = "env_conf/.check_osm_life_cycle_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    print(get_osm_potentially_open(args.area))
