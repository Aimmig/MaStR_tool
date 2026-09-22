from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from dotenv import load_dotenv
from get_mastr_data_by_ref import get_data

if __name__ == "__main__":
    env_file = "env_conf/.check_osm_life_cyle_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    osm_units = getWindPlantsInArea(args.area,
                                    sanitize=True)
    CONSTRUCTION_POWER = "construction:power"
    REF_MASTR = "ref:mastr"
    tags = osm_units[[REF_MASTR, CONSTRUCTION_POWER]].dropna(subset=[REF_MASTR, CONSTRUCTION_POWER])
    refs = tags[REF_MASTR].to_list()
    cols = ["Inbetriebnahmedatum", "Laengengrad", "Breitengrad"]
    construction_now_open = get_data("wind", refs, cols)
    print(construction_now_open)
