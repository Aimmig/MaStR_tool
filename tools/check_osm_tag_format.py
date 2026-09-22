from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from utils.CheckOsmTagFormats import check_tags
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv("env_conf/.check_osm_env")
    parser = createOSMFormatParser()
    args = parser.parse_args()
    check_col = args.tag
    osm_units = getWindPlantsInArea(args.area,
                                    sanitize=True)
    filtered, cols = check_tags(osm_units, check_col, strict=True)
    output = None
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
