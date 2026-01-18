from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getPlantsWithinArea
from utils.Helper import plot

if __name__ == "__main__":
    parser = createOSMFormatParser()
    arguments = parser.parse_args()
    output = arguments.output
    osm_pbf = arguments.source
    osm_units = getPlantsWithinArea(osm_pbf)
    test_col = 'generator:output:electricity'
    known_good = "small_installation|MW|kW|yes"
    unusual = osm_units[~osm_units[test_col].str.contains(known_good, na=False)].dropna(subset=[test_col])
    print_cols = ['id', 'model', 'generator:output:electricity']
    csv = unusual[print_cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
    plot('model', print_cols, unusual)
