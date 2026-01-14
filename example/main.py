import argparse
import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as PlantFilter
from utils.PostProcessing import PostProcessing
from utils.PreConfiguredParser import createParser
import pandas as pd


def getData(args) -> pd.DataFrame:
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    cols = PostProcessing.createColumnDict(args)
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
    return plants


if __name__ == "__main__":
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    parser = createParser()
    args = parser.parse_args()
    plants = getData(args)
    PostProcessing.printData(args, plants)
