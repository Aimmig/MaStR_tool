from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
import ast
from dotenv import load_dotenv

if __name__ == "__main__":
    env_file = "env_conf/.check_osm_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    #check_col = args.tag
    osm_units = getWindPlantsInArea(args.area,
                                    sanitize=True)
    print(osm_units.columns)
    tags = osm_units[["ref:mastr","construction:power"]].dropna(subset=["ref:mastr","construction:power"])
    print(" ".join(tags["ref:mastr"].to_list()))
