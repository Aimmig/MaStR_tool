from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from utils.CheckOsmTagFormats import check_tags
from dotenv import load_dotenv


def get_filtered_tags(area, check_col):
    osm_units = getWindPlantsInArea(area, sanitize=True)
    filtered, cols = check_tags(osm_units, check_col, strict=True)
    output = None
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    return csv


if __name__ == "__main__":
    env_file = "env_conf/.check_osm_env"
    load_dotenv(env_file)
    parser = createOSMFormatParser()
    args = parser.parse_args()
    check_col = args.tag
    area = args.area
    csv = get_filtered_tags(area, check_col)
    if csv:
        print(csv)
