import os
from utils.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as PlantFilter
from utils.PostProcessing import PostProcessing
from utils.Helper import get_cols_without_geometry
from utils.Helper import check_cols_in_dataframe
from utils.Helper import plot, test_against_OSM, print_test_summary
from utils.PreConfiguredParser import createParser
from utils.PlantsFromOSM import getPlantsWithinArea
from utils.Constants import SELECT_COLS
import geopandas as gpd


def getData(args) -> gpd.GeoDataFrame:
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    plants = Mastrdata(args.source).df

    if args.query:
        plants = plants.query(args.query)
    if args.discardSmall:
        plants = PlantFilter.get_without_small(plants, args.discardSmall)
    if args.startDate:
        plants = PlantFilter.get_plants_with_start_date(plants)
    if args.endDate:
        plants = PlantFilter.get_plants_with_end_date(plants)
    if args.openingDate:
        plants = PlantFilter.get_plants_with_opening_date(plants)
    if args.openingDatePast:
        plants = PlantFilter.get_plants_with_past_opening_date(plants)
    if args.openingDateFuture:
        plants = PlantFilter.get_plants_with_future_opening_date(plants)
    if args.currentlyOperational:
        plants = PlantFilter.get_plants_currently_operational(plants)
    if args.onshore:
        plants = PlantFilter.get_onshore(plants)
    if args.offshore:
        plants = PlantFilter.get_offshore(plants)
    if args.eeg:
        plants = PlantFilter.get_EEG(plants)
    if args.kwk:
        plants = PlantFilter.get_KWK(plants)
    if args.formatManufacturer:
        plants = PostProcessing.format_manufacturer(plants, "Hersteller")

    cols_to_keep = check_cols_in_dataframe(plants, args.keepColumns)
    plants = PostProcessing.format_power(plants, args.formatPower)
    plants = PostProcessing.translate(plants, cols_to_keep)
    return plants, get_cols_without_geometry(cols_to_keep)


if __name__ == "__main__":
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    parser = createParser()
    arguments = parser.parse_args()
    mastr_units, cols = getData(arguments)
    plot(arguments.plot, cols, mastr_units)
    csv = mastr_units[cols].to_csv(
                arguments.output,
                index=False,
                )
    if csv:
        print(csv)
    if arguments.testagainstOSM:
        osm_pbf = arguments.testagainstOSM[0]
        check_col = None
        if len(arguments.testagainstOSM) > 1:
            check_col = arguments.testagainstOSM[1]
            check_col = SELECT_COLS[check_col]
        distance = 50
        osm_units = getPlantsWithinArea(osm_pbf, sanitize=True)
        # osm_units[['id', 'end_date']].to_csv("dates.csv")
        joined, cols = test_against_OSM(check_col, osm_units,
                                        mastr_units, max_dist=distance)
        plot("dist", cols, joined)
        # print(list(joined))
        mastr_diff = joined[~(joined["ref:mastr_osm"] == joined["ref:mastr_mastr"])]
        mastr_diff = mastr_diff[["ref:mastr_osm", "ref:mastr_mastr", "id"]][mastr_diff["ref:mastr_osm"].notnull()]
        mastr_diff["id"] = mastr_diff["id"].astype(int)
        mastr_diff["ref:mastr_osm"] = mastr_diff["ref:mastr_osm"].astype(str)
        mastr_diff["ref:mastr_mastr"] = mastr_diff["ref:mastr_mastr"].astype(str)
        # print(mastr_diff)
        # print(mastr_diff.shape[0])
        print_test_summary(distance,
                           joined, mastr_units, osm_units,
                           check_col, arguments.formatPower,
                           )
        joined[["lat_mastr", "lon_mastr", "ref:mastr_mastr", check_col+"_mastr", check_col+"_osm"]].to_csv("result.csv", index=False)
