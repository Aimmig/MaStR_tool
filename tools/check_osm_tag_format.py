from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from utils.CheckOsmTagFormats import check_tags
from utils.Helper import plot


if __name__ == "__main__":
    parser = createOSMFormatParser()
    args = parser.parse_args()
    check_col = args.tag
    osm_units = getWindPlantsInArea(args.area,
                                    sanitize=True,
                                    invalidate_cache=False)
    filtered, cols = check_tags(osm_units, check_col)
    output = None
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
