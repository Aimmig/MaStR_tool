from open_mastr import Mastr
import pandas as pd
import geopandas as gpd
from utils.DataFilter import DataFilter as PlantFilter
from utils.PostProcessing import PostProcessing
from utils.Helper import get_cols_without_geometry
from utils.Helper import check_cols_in_dataframe
import geopandas as gpd


class Mastrdata:

    def __init__(self, energy_carrier: str):

        """
        Downloads the Mastr unit data and filters for the given technology.
        Large parts of data is thrown away since it's not really relevant,
        also throws away lots of empty columns which are empty.

        Parameters:
        energy_carrier: The energy carrier to download
        """

        # download relevant data with api
        db = Mastr()
        db.download(data=energy_carrier, api_data_types=["unit_data"],
                    api_location_type=["location_elec_generation"])

        # get the required tables
        table = energy_carrier + "_extended"
        df_extended = Mastrdata.get_dataFrame(db, table)

        table = energy_carrier + "_eeg"
        df_eeg = Mastrdata.get_dataFrame(db, table)

        key = 'EegMastrNummer'
        # TO-DO:
        # Adapt this join to also work properly with plants
        # where no 1 to 1 matching exists between both tables.
        # Often one plant consists of multiple generators.
        # In these cases the extended table contains all individual
        # units and the eeg table contains the aggregated plant
        # that these generators are part of.
        df = df_extended.merge(df_eeg, on=key, how='left',
                               suffixes=('', '_DROP')).filter(
                                       regex='^(?!.*_DROP)')

        # filter data before further processing
        df = df.dropna(axis=1, how='all')
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df.Laengengrad, df.Breitengrad),
            crs="EPSG:4326",
        )
        self.df = gdf

    @staticmethod
    def get_dataFrame(db: Mastr, table: str) -> pd.DataFrame:

        """
        Helper Method to get one table from the database
        """

        df = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
        df = pd.read_sql(sql=table, con=db.engine)
        return df


def download(source: str) -> pd.DataFrame:
    """
    Wrapper function that only downloads the MaStR data.
    Returns: The pandas DataFrame
    """
    return Mastrdata(source).df


def get_filtered_mastr_from_args(args):
    return get_filtered_mastr_data(args.source, args.keepColumns, args.query, args.discardSmall,
                                   args.startDate, args.endDate,
                                   args.openingDate, args.openingDatePast,
                                   args.openingDateFuture, args.currentlyOperational,
                                   args.onshore, args.offshore,
                                   args.eeg, args.kwk,
                                   args.formatManufacturer, args.formatPower,
                                   )


def get_filtered_mastr_data(source, keepColumns, query=None, discardSmall=None,
                            startDate=False, endDate=False,
                            openingDate=False, openingDatePast=False,
                            openingDateFuture=False, currentlyOperational=False,
                            onshore=False, offshore=False,
                            eeg=False, kwk=False,
                            formatManufacturer=False, formatPower=False,
                            ) -> gpd.GeoDataFrame:
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    plants = download(source)

    # evaluate all args and apply the correct functions
    if query:
        plants = plants.query(query)
    if discardSmall:
        plants = PlantFilter.get_without_small(plants, discardSmall)
    if startDate:
        plants = PlantFilter.get_plants_with_start_date(plants)
    if endDate:
        plants = PlantFilter.get_plants_with_end_date(plants)
    if openingDate:
        plants = PlantFilter.get_plants_with_opening_date(plants)
    if openingDatePast:
        plants = PlantFilter.get_plants_with_past_opening_date(plants)
    if openingDateFuture:
        plants = PlantFilter.get_plants_with_future_opening_date(plants)
    if currentlyOperational:
        plants = PlantFilter.get_plants_currently_operational(plants)
    if onshore:
        plants = PlantFilter.get_onshore(plants)
    if offshore:
        plants = PlantFilter.get_offshore(plants)
    if eeg:
        plants = PlantFilter.get_EEG(plants)
    if kwk:
        plants = PlantFilter.get_KWK(plants)
    if formatManufacturer:
        plants = PostProcessing.format_manufacturer(plants, "Hersteller")
    if formatPower:
        plants = PostProcessing.format_power(plants, formatPower)

    plants = PostProcessing.format_model(plants, "Typenbezeichnung")
    if keepColumns:
        cols_to_keep = check_cols_in_dataframe(plants, keepColumns)
    else:
        cols_to_keep = None
    plants = PostProcessing.translate(plants, cols_to_keep)
    return plants, get_cols_without_geometry(cols_to_keep)
