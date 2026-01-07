from open_mastr import Mastr
import pandas as pd

selected_cols = [
        'Technologie', 'WindAnLandOderAufSee',
        'Bundesland','Landkreis','Gemeinde',
        'Laengengrad', 'Breitengrad',
        'NameWindpark','Hersteller','Typenbezeichnung','Nabenhoehe', 'Rotordurchmesser',
        'EegMastrNummer', 'Nettonennleistung', 'NameStromerzeugungseinheit',
        'GeplantesInbetriebnahmedatum', 'Inbetriebnahmedatum', 'DatumEndgueltigeStilllegung', 'DatumDownload'
]

print_cols = [
        'Gemeinde',
        'NameWindpark','Hersteller',
        'Nettonennleistung', 'NameStromerzeugungseinheit',
        'GeplantesInbetriebnahmedatum', 'Inbetriebnahmedatum', 'DatumEndgueltigeStilllegung' 
]

# download relevant data
db = Mastr()
db.download(data="wind",api_data_types=["unit_data"],api_location_type=["location_elec_generation"])

# generate a list of all tables
table="wind_extended"
df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con=db.engine)
df = pd.read_sql(sql=table, con=db.engine)

# filter data before further processing 
df.dropna(axis=1,how='all',inplace=True)
df = df[selected_cols]
# only onshore regular power plants considered
df = df.loc[
    (df["WindAnLandOderAufSee"] == "Windkraft an Land") & 
    (df["Technologie"] == "Horizontalläufer") &
    (df["Nettonennleistung"] > 600)]

df = df[df["Bundesland"] == "Rheinland-Pfalz"]
#df = df[df["Gemeinde"] == "Gau-Bickelheim"]
df = df[df["DatumEndgueltigeStilllegung"].notnull()]
#df = df[df["GeplantesInbetriebnahmedatum"].notnull()]
#df = df[df["Inbetriebnahmedatum"].notnull()]
print(df[print_cols])
