from open_mastr import Mastr
import pandas as pd
from datetime import date

# map to translate only the acutally used columns
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
        'EegMastrNummer': 'ref:eeg',
        'Hersteller': 'manufacturer', 'Typenbezeichnung': 'model',
        'Nabenhoehe': 'height:hub', 'Rotordurchmesser': 'rotor:diameter'
        }

# columns used for printing/debuging
print_cols = [
        'lon', 'lat',
        'output', 'name_unit', 'ref:eeg',
        'opening_date', 'start_date', 'end_date'
]

today = date.today().isoformat()


# select only data within some area
def filter_region(df, state=None, county=None, municipality=None):
    if state:
        df = df[df["state"] == state]
    if county:
        df = df[df["county"] == county]
    if municipality:
        df = df[df["municipality"] == municipality]
    return df


def get_prefiltered_Mastr(on_or_offshore="Windkraft an Land",
                          technology="Horizontalläufer", output=600):

    # download relevant data
    db = Mastr()
    db.download(data="wind", api_data_types=["unit_data"],
                api_location_type=["location_elec_generation"])

    # generate a list of all tables
    table = "wind_extended"
    df = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
    df = pd.read_sql(sql=table, con=db.engine)
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


def get_plants_with_end_date(df):
    return df[df["end_date"].notnull()]


def get_plants_with_start_date(df):
    return df[df["start_date"].notnull()]


def get_plants_with_opening_date(df):
    return df[df["opening_date"].notnull()]


def get_plants_with_future_end_date(df):
    return df[df["end_date"] > today]


def get_plants_with_past_end_date(df):
    return df[df["end_date"] < today]


def get_plants_with_future_opening_date(df):
    return df[df["opening_date"] > today]


def get_plants_with_past_opening_date(df):
    return df[df["opening_date"] < today]


def get_plants_with_past_start_date(df):
    return df[df["start_date"] < today]


# only for completion this should always return an empty df
def get_plants_with_future_start_date(df):
    return df[df["start_date"] > today]


if __name__ == '__main__':
    df = get_prefiltered_Mastr()
    df = filter_region(df, state="Rheinland-Pfalz")
    # df = get_plants_with_past_start_date(df)
    df = get_plants_with_past_end_date(df)
    print(df[print_cols])
