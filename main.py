from open_mastr import Mastr
import pandas as pd

used_cols={
        'Technologie': 'technology', 'WindAnLandOderAufSee': 'on_or_offshore',
        'Bundesland': 'state' ,'Landkreis': 'county', 'Gemeinde': 'municipality',
        'GeplantesInbetriebnahmedatum': 'opening_date', 'Inbetriebnahmedatum': 'start_date',
        'DatumEndgueltigeStilllegung': 'end_date', 'DatumDownload': 'check_date',
        'NameWindpark': 'name_windfarm', 'Nettonennleistung': 'output', 'NameStromerzeugungseinheit': 'name_unit',
        'Laengengrad': 'lon', 'Breitengrad': 'lat', 'EegMastrNummer': 'ref:eeg',
        'Hersteller': 'manufacturer', 'Typenbezeichnung': 'model', 'Nabenhoehe': 'height:hub', 'Rotordurchmesser': 'rotor:diameter'
        }

print_cols = [
        'lon', 'lat',
        'output', 'name_unit', 'ref:eeg',
        'opening_date', 'start_date', 'end_date'
]

# download relevant data
db = Mastr()
db.download(data="wind",api_data_types=["unit_data"],api_location_type=["location_elec_generation"])

# generate a list of all tables
table="wind_extended"
df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con=db.engine)
df = pd.read_sql(sql=table, con=db.engine)

#rename columns to better match osm tags
df = df.rename(columns=used_cols)

# filter data before further processing 
df.dropna(axis=1,how='all',inplace=True)

df = df[list(used_cols.values())]
# only onshore regular power plants considered
df = df.loc[
    (df["on_or_offshore"] == "Windkraft an Land") &
    (df["technology"] == "Horizontalläufer") &
    (df["output"] > 600)]

df = df[df["state"] == "Rheinland-Pfalz"]
#df = df[df["municipality"] == "Gau-Bickelheim"]
#df = df[df["end_date"].notnull()]
#df = df[df["end_date"] >= "2024-01-01"]
df = df[df["opening_date"].notnull()]
#df = df[df["start_date"].notnull()]
print(df[print_cols])
