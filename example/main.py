import argparse
import os
from energycarrier.Mastrdata import Mastrdata
from utils.Constants import SELECT_COLS
from utils.DataFilter import DataFilter as PlantFilter
from utils.PostProcessing import PostProcessing
from utils.PostProcessing import get_cols_without_geometry
from utils.PostProcessing import check_cols_in_dataframe
from utils.PostProcessing import check_strict
from utils.PreConfiguredParser import createParser
from utils.PlantsFromOSM import getPlantsWithinArea
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


def plot(plot_args: str, cols_popup: list[str], plants: gpd.GeoDataFrame):
    main_col = None
    if plot_args:
        if plot_args == "year":
            main_col = "year"
            plants["year"] = plants['start_date'].dt.year
        elif plot_args == "dist":
            main_col = "dist"
        else:
            main_col = SELECT_COLS[plot_args]
        plotted_map = plants.explore(
            column=main_col,
            popup=cols_popup,
            )
        plotted_map.save('map.html')


def test_against_OSM(match_col: str, osm: gpd.GeoDataFrame,
                     mastr_units: gpd.GeoDataFrame, max_dist: int):
    # set proper crs
    crs_str = "ESRI:102003"
    osm_to_join = osm_units.to_crs(crs_str)
    mastr_to_join = mastr_units.to_crs(crs_str)
    # spatial join with options, keep mastr geometry
    osm_vs_mastr = mastr_to_join.sjoin_nearest(
        osm_to_join,
        how='left',
        lsuffix='mastr',
        rsuffix='osm',
        max_distance=max_dist,
        distance_col="dist",
        )
    cols = list(osm_vs_mastr.columns.values).remove("geometry")
    # here only keep missmatches from sjon_nearest
    if match_col is None:
        no_match = osm_vs_mastr[osm_vs_mastr["dist"].isnull()].fillna("dist")
        return no_match, cols
    # only keep result with non-zero distance. aka only good results
    osm_vs_mastr = osm_vs_mastr.query("dist > 0")
    # rename the column to match namespace
    match_col = SELECT_COLS[match_col]
    # check for strict matches on specified column
    return check_strict(osm_vs_mastr, match_col), cols


def print_test_summary(dist: int, joined, mastr, osm, check_col, power):
    print("----OSM vs MaStR matches, also see generated map------")
    if check_col:
        check_col = SELECT_COLS[check_col]
        settings = "----Settings: " + str(dist) + " with " + check_col
    else:
        settings = "----Settings: " + str(dist) + " only no matches---"
    if check_col == "generator:output:electricity":
        settings += " with " + power
    print(settings)
    print("Size OSM  : " + str(osm.shape[0]))
    print("Size MaStR: " + str(mastr.shape[0]))
    print("Matches   : " + str(joined.shape[0]))
    perc_osm = 100*joined.shape[0]/osm.shape[0]
    perc_mastr = 100*joined.shape[0]/mastr.shape[0]
    print("Matches   : " + str(perc_osm) + " %")
    print("Matches   : " + str(perc_mastr) + " %")
    print("---Note: Size of MaStR and % is AFTER filtering----")
    return


if __name__ == "__main__":
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    parser = createParser()
    arguments = parser.parse_args()
    mastr_units, cols = getData(arguments)
    plot(arguments.plot, cols, mastr_units)
    if arguments.output:
        csv = mastr_units[cols].to_csv(
                arguments.output,
                index=False,
                )
    if arguments.testagainstOSM:
        osm_pbf = arguments.testagainstOSM[0]
        check_col = None
        if len(arguments.testagainstOSM) > 1:
            check_col = arguments.testagainstOSM[1]
        distance = 50
        osm_units = getPlantsWithinArea(osm_pbf)
        osm_units["geometry"].to_csv("geometry_osm.csv")
        joined, cols = test_against_OSM(check_col, osm_units,
                                        mastr_units, max_dist=distance)
        joined["ref:mastr"].to_csv("osm"+str(check_col or '')+".csv", index=False)
        plot("dist", cols, joined)
        print_test_summary(distance,
                           joined, mastr_units, osm_units,
                           check_col, arguments.formatPower,
                           )
