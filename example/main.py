import argparse
import os
from energycarrier.Mastrdata import Mastrdata
from utils.Constants import SELECT_COLS
from utils.DataFilter import DataFilter as PlantFilter
from utils.PostProcessing import PostProcessing
from utils.PostProcessing import get_cols_without_geometry
from utils.PostProcessing import check_cols_in_dataframe
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
        else:
            main_col = SELECT_COLS[plot_args]
        plotted_map = plants.explore(
            column=main_col,
            popup=cols_popup,
            )
        plotted_map.save('map.html')


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
