from open_mastr import Mastr
import pandas as pd
from datetime import date

# map to translate only the acutally used columns
# might be adapted to include more data or to throw away unwanted columns
used_cols = {
        'Technologie': 'technology', 'WindAnLandOderAufSee': 'on_or_offshore',
        'Bundesland': 'state', 'Landkreis': 'county',
        'Gemeinde': 'municipality',
        'GeplantesInbetriebnahmedatum': 'opening_date',
        'Inbetriebnahmedatum': 'start_date',
        'DatumEndgueltigeStilllegung': 'end_date',
        'DatumDownload': 'check_date',
        'NameWindpark': 'name_windfarm', 'Nettonennleistung': 'output',
        'NameStromerzeugungseinheit': 'name_unit',
        'Laengengrad': 'lon', 'Breitengrad': 'lat',
        'EinheitMastrNummer': 'ref:MaStR',
        'AnlagenschluesselEeg': 'ref:EEG',
        'Hersteller': 'manufacturer', 'Typenbezeichnung': 'model',
        'Nabenhoehe': 'height:hub', 'Rotordurchmesser': 'rotor:diameter'
        }

# columns used for printing/debuging
print_cols = [
        'lon', 'lat', 'output', 'ref:MaStR', 'ref:EEG',
        'opening_date', 'start_date', 'end_date'
]

today = date.today().isoformat()


def filter_region(df, state=None, county=None, municipality=None):
    """
    Filter data by some regional property

    Parameters:
    df: The dataframe to filter on.
    state: The state which should be included.
    county: The county which should be included.
    municipality: The municipality which should be included.

    Returns:
    The filtered dataframe
    """

    if state:
        df = df[df["state"] == state]
    if county:
        df = df[df["county"] == county]
    if municipality:
        df = df[df["municipality"] == municipality]
    return df


def get_prefiltered_Mastr(on_or_offshore="Windkraft an Land",
                          technology="Horizontalläufer", output=600):

    """
    Downloads the Mastr unit data and filters by the given technolgy,
    On/Offshore and power output. Translates the colums to be shorter names
    and more closer to usefull osm tags. Large parts of data is thrown away
    since it's not really relevant, also throws away lot's of empty columns
    which are always empty for wind power plants.

    Parameters:
    on_or_offshore: either "Windkraft an Land" or "Windkraft auf See"
    technoly: either "Horizontalläufer" or "Vertikalläufer"
    output: the nominal power output of the plant. Exclude small plants.

    Returns: Dataframe which contains the pre filtered Mastr data for
    wind power plants
    """

    # download relevant data with api
    db = Mastr()
    db.download(data="wind", api_data_types=["unit_data"],
                api_location_type=["location_elec_generation"])

    # get the required tables
    table = "wind_extended"
    df_extended = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
    df_extended = pd.read_sql(sql=table, con=db.engine)

    table = "wind_eeg"
    df_eeg = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
    df_eeg = pd.read_sql(sql=table, con=db.engine)

    # join on the internaly used key
    key = 'EegMastrNummer'
    # join and remove some duplicate columns which
    df = df_extended.merge(df_eeg, on=key, how='inner',
                           suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

    # rename columns to better match osm tags
    df = df.rename(columns=used_cols)
    # filter data before further processing
    df.dropna(axis=1, how='all', inplace=True)
    df = df[list(used_cols.values())]

    # filter according to given or default values which are considered
    df = df.loc[
        (df["on_or_offshore"] == on_or_offshore) &
        (df["technology"] == technology) &
        (df["output"] > output)]
    return df


# ---- Basic filters based on NaT ------

def get_plants_with_(df, date_type):
    """Template function to filter for plants that have
    the specified date_tye present. Also sorts data for
    convenience

    Parameter:
    date_type: Either "end_date", "start_date", "opening_date"

    Returns:
    Sorted dataframe with plants with selected date_type present
    """
    return df[df[date_type].notnull()].sort_values(date_type)


def get_plants_with_end_date(df):
    """Return only plants with known end_date.
    (Planed) Decommissioning can be safely assumed.
    This date can safely be assumed to be in the past.
    """
    return get_plants_with_(df, "end_date")


def get_plants_with_start_date(df):
    """Return only plants with known start_date.
    This date can safely be assumed to be in the past.
    Note this includes plant that already out of operation again.
    """
    return get_plants_with_(df, "start_date")


def get_plants_with_opening_date(df):
    """Return only plants with known opening_date.
    Note this might include plants which should have openend,
    but still are not in operation."""
    return get_plants_with_(df, "opening_date")


# ---- Basic filters based on comparison with todays date -----

def get_plants_with_future_opening_date(df):
    """Return only plants which are expected to open."""
    return df[df["opening_date"] > today]


def get_plants_with_past_opening_date(df):
    """Return only plants that should have opened
    but still aren't operational.
    This could mean any form delay, or it was never built at all.
    """
    return df[df["opening_date"] < today]


def get_plants_currently_operational(df):
    """Return only plants that are currently in operation.
    This means plants that are going to opened are excluded,
    and plants which are permanently closed.
    Note that short closures which are contained in the
    full data set are still included here, as these aren't
    relevant for this purpose.
    """
    df = df.loc[
        (df["opening_date"].isnull()) &
        (df["end_date"].isnull())]
    return df


if __name__ == '__main__':
    df = get_prefiltered_Mastr()
    # df = filter_region(df, state="Rheinland-Pfalz")
    df = get_plants_with_end_date(df)

    print(df[print_cols])
