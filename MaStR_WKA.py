from open_mastr import Mastr
from MaStR_EEG_Base import MaStR_EEG_Base
import pandas as pd
from datetime import date
import operator

today = date.today().isoformat()

class MaStR_WKA(MaStR_EEG_Base):
    
    # columns used for printing/debuging
    # TO-DO move common tags to parent class
    print_cols = [
        'lon', 'lat', 'ref:mastr', 'ref:EEG',
        'opening_date', 'start_date', 'end_date',
        'generator:output:electricity'
    ]

    # map to translate only the acutally used columns
    # might be adapted to include more data or to throw away unwanted columns
    # TO-DO move common tags to parent class
    used_cols = {     
        'Bundesland': 'state', 'Landkreis': 'county',
        'Gemeinde': 'municipality',
        'GeplantesInbetriebnahmedatum': 'opening_date',
        'Inbetriebnahmedatum': 'start_date',
        'DatumEndgueltigeStilllegung': 'end_date',
        'Laengengrad': 'lon', 'Breitengrad': 'lat',
        'DatumDownload': 'check_date',
        'EinheitMastrNummer': 'ref:mastr',
        'AnlagenschluesselEeg': 'ref:EEG',
        'NameStromerzeugungseinheit': 'name_unit',
        'Technologie': 'technology', 'WindAnLandOderAufSee': 'on_or_offshore',
        'NameWindpark': 'name_windfarm',
        'Nettonennleistung': 'generator:output:electricity',
        'Hersteller': 'manufacturer', 'Typenbezeichnung': 'model',
        'Nabenhoehe': 'height:hub', 'Rotordurchmesser': 'rotor:diameter'
    }


    def __init__(self):
        super().__init__("wind")
        # rename columns to better match osm tags
        self.df = self.df.rename(columns=self.used_cols)
        self.df = self.df[list(self.used_cols.values())]

    def preFilter(self, on_or_offshore="Windkraft an Land",
                          technology="Horizontalläufer", output=600):

        """
        Filters by the given technolgy, On/Offshore and power output.
        Translates the colums to be shorter names and more closer to usefull osm tags.

        Parameters:
        on_or_offshore: either "Windkraft an Land" or "Windkraft auf See"
        technoly: either "Horizontalläufer" or "Vertikalläufer"
        output: the nominal power output of the plant. Exclude small plants.
        """

        # filter according to given or default values which are considered
        self.df = self.df.loc[
            (self.df["on_or_offshore"] == on_or_offshore) &
            (self.df["technology"] == technology) &
            (self.df["generator:output:electricity"] > output)]

        unit_cols = ["generator:output:electricity"]
        self.df[unit_cols] = self.df[unit_cols].astype(int)
        self.df["generator:output:electricity"] = self.df["generator:output:electricity"].astype(str) + " kW"
