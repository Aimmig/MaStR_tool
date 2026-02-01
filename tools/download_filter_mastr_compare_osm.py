import os
from utils.Mastrdata import get_filtered_mastr_from_args
from utils.Helper import plot, test_against_OSM, print_test_summary
from utils.Helper import get_existing_ref_missmatch
from utils.Helper import get_without_osm_ref
from utils.PreConfiguredParser import createParser
from utils.PlantsFromOSM import getWindPlantsInArea
from utils.Constants import SELECT_COLS, LON, LAT
from utils.Constants import REF_MASTR_MASTR, MASTR_SUFFIX, OSM_SUFFIX
import geopandas as gpd


if __name__ == "__main__":
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    parser = createParser()
    arguments = parser.parse_args()
    mastr_units, cols = get_filtered_mastr_from_args(arguments)
    plot(arguments.plot, cols, mastr_units)
    csv = mastr_units[cols].to_csv(
                None,
                index=False,
                )
    if csv and not arguments.testagainstOSM:
        print(csv)
    # TO-DO Decouple the following from the previous
    if arguments.testagainstOSM:
        osm_pbf = arguments.testagainstOSM
        if arguments.keepColumns is None or len(arguments.keepColumns) != 1:
            raise ValueError("Only exactly one column supported when testosm is set")
        check_col = "".join(arguments.keepColumns)
        check_col = SELECT_COLS[check_col]
        # settings
        distance = 50
        # date_format = "%Y/%m"
        # date_format = "%d.%m.%Y"
        date_format = "%Y-%m-%d"
        osm_units = getWindPlantsInArea(osm_pbf,
                                        sanitize=True, invalidate_cache=True,
                                        date_format=date_format)
        joined, cols = test_against_OSM(check_col, osm_units,
                                        mastr_units, max_dist=distance,
                                        strict=False)
        plot("dist", cols, joined)
        mastr_diff = get_existing_ref_missmatch(joined)
        # print(mastr_diff)
        joined = get_without_osm_ref(joined)
        # print_test_summary(distance,
        #                   joined, mastr_units, osm_units,
        #                   check_col, arguments.formatPower,
        #                   )

        if REF_MASTR_MASTR in list(joined.columns.values):
            mastr_col_sel = [LAT+MASTR_SUFFIX, LON+MASTR_SUFFIX, REF_MASTR_MASTR]
        else:
            mastr_col_sel = [LAT+MASTR_SUFFIX, LON+MASTR_SUFFIX]
        if check_col:
            mastr_col_sel += [check_col+MASTR_SUFFIX, check_col+OSM_SUFFIX]
        csv = joined[mastr_col_sel].to_csv(None, index=False)
        if csv:
            print(csv)
