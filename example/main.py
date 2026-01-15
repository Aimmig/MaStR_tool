import argparse
import os
from energycarrier.Mastrdata import Mastrdata
from utils.Constants import SELECT_COLS
from utils.DataFilter import DataFilter as PlantFilter
from utils.PostProcessing import PostProcessing
from utils.PostProcessing import get_cols_without_geometry
from utils.PreConfiguredParser import createParser
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
        plants = PostProcessing.format_manufacturer(plants)

    plants = PostProcessing.format_power(plants, args.formatPower)
    plants = PostProcessing.translate(plants, args.keepColumns)
    return plants


def plot(args, plants: gpd.GeoDataFrame):
    cols_popup = get_cols_without_geometry(args.keepColumns)
    main_col = None
    if args.plot:
        if args.plot == "year":
            main_col = "year"
            plants["year"] = plants['start_date'].dt.year
        else:
            main_col = SELECT_COLS[args.plot]
        plotted_map = plants.explore(
            column=main_col,
            popup=cols_popup,
            )
        plotted_map.save('map.html')


if __name__ == "__main__":
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    parser = createParser()
    arguments = parser.parse_args()
    mastr_units = getData(arguments)
    plot(arguments, mastr_units)
    cols_to_keep = get_cols_without_geometry(arguments.keepColumns)
    if arguments.output:
        csv = mastr_units[cols_to_keep].to_csv(
                arguments.output,
                index=False,
                )
