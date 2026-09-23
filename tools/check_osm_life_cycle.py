from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from dotenv import load_dotenv
from get_mastr_data_by_ref import get_data

CONSTRUCTION_POWER = "construction:power"
PLANNED_POWER = "planned:power"
DESC_CONSTR = "under construction"
REF_MASTR = "ref:mastr"


def filter_for_construction(df):
    tags = df.loc[(df[CONSTRUCTION_POWER] == 'generator') | (df['description'] == DESC_CONSTR) | (df[PLANNED_POWER] == 'generator')]
    return tags[REF_MASTR].dropna().to_list()

if __name__ == "__main__":
    env_file = "env_conf/.check_osm_life_cycle_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    osm_units = getWindPlantsInArea(args.area,
                                    sanitize=True)
    cols = ["Inbetriebnahmedatum", "Laengengrad", "Breitengrad"]
    refs = filter_for_construction(osm_units)
    construction_now_open = get_data("wind", refs, cols)
    print(construction_now_open)
