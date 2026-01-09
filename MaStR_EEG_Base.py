from open_mastr import Mastr
import pandas as pd
from datetime import date
import operator

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
        'NameWindpark': 'name_windfarm',
        'Nettonennleistung': 'generator:output:electricity',
        'NameStromerzeugungseinheit': 'name_unit',
        'Laengengrad': 'lon', 'Breitengrad': 'lat',
        'EinheitMastrNummer': 'ref:MaStR',
        'AnlagenschluesselEeg': 'ref:EEG',
        'Hersteller': 'manufacturer', 'Typenbezeichnung': 'model',
        'Nabenhoehe': 'height:hub', 'Rotordurchmesser': 'rotor:diameter'
        }

# columns used for printing/debuging
print_cols = [
        'lon', 'lat', 'ref:MaStR',
        'opening_date', 'start_date', 'end_date',
        'generator:output:electricity'
        ]


today = date.today().isoformat()

class MaStR_EEG_Base:
    def __init__(self, energy_carrier):
       
        """
        Downloads the Mastr unit data and filters for the given technology.
        Large parts of data is thrown away since it's not really relevant,
        also throws away lot's of empty columns which are empty.

        Parameters:
        energy_carrier: The energy carrier to download
        """
        
        # download relevant data with api
        db = Mastr()
        db.download(data=energy_carrier, api_data_types=["unit_data"],
                api_location_type=["location_elec_generation"])
        # get the required tables
        table = energy_carrier+ "_extended"
        df_extended = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
        df_extended = pd.read_sql(sql=table, con=db.engine)

        table = energy_carrier+ "_eeg"
        df_eeg = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
        df_eeg = pd.read_sql(sql=table, con=db.engine)

        # join on the internaly used key
        key = 'EegMastrNummer'
        # join and remove some duplicate columns which
        df = df_extended.merge(df_eeg, on=key, how='inner',
                           suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

    
        # filter data before further processing
        df.dropna(axis=1, how='all', inplace=True)
        self.df = df

    def filter_region(self, state=None, county=None, municipality=None):
        """
        Filter data by some regional property

        Parameters:
        state: The state which should be included.
        county: The county which should be included.
        municipality: The municipality which should be included.

        Returns:
        The filtered dataframe
        """

        if state:
            self.df = self.df[self.df["state"] == state]
        if county:
            self.df = self.df[self.df["county"] == county]
        if municipality:
            self.df = self.df[self.df["municipality"] == municipality]
        return self.df

    def get_all(self):
        return self.df

    # ---- Basic filters based on NaT ------

    def get_plants_with_(self, date_type):
        """Template function to filter for plants that have
        the specified date_tye present. Also sorts data for
        convenience

        Parameter:
        date_type: Either "end_date", "start_date", "opening_date"

        Returns:
        Sorted dataframe with plants with selected date_type present
        """
        return self.df[self.df[date_type].notnull()]


    def get_plants_with_end_date(self):
        """Return only plants with known end_date.
        (Planed) Decommissioning can be safely assumed.
        This date can safely be assumed to be in the past.
        """
        return self.get_plants_with_("end_date")


    def get_plants_with_start_date(self):
        """Return only plants with known start_date.
        This date can safely be assumed to be in the past.
        Note this includes plant that already out of operation again.
        """
        return self.get_plants_with_("start_date")


    def get_plants_with_opening_date(self, comp=None, date=today):
        """Return only plants with known opening_date.
        Note this might include plants which should have openend,
        but still are not in operation.

        Parameters:
        comp: Optionally comparison parameter to filter
        date: Optionally the date to compare with
        """
        self.df = self.get_plants_with_("opening_date")
        if comp:
            return self.df[comp(self.df["opening_date"], date)]
        return self.df


    # ---- Basic filters based on comparison with todays date -----

    def get_plants_with_future_opening_date(self):
        """Return only plants which are expected to open."""
        return self.get_plants_with_opening_date(operator.gt)


    def get_plants_with_past_opening_date(self):
        """Return only plants that should have opened
        but still aren't operational.
        This could mean any form delay, or it was never built at all.
        """
        return self.get_plants_with_opening_date(operator.lt)


    def get_plants_currently_operational(self):
        """Return only plants that are currently in operation.
        This means plants that are going to opened are excluded,
        and plants which are permanently closed.
        Note that short closures which are contained in the
        full data set are still included here, as these aren't
        relevant for this purpose.
        """
        self.df = self.df.loc[
            (self.df["opening_date"].isnull()) &
            (self.df["end_date"].isnull())].sort_values("start_date")
        return self.df


class MaStR_WKA(MaStR_EEG_Base):
    def __init__(self):
        super().__init__("wind")
        # rename columns to better match osm tags
        self.df = self.df.rename(columns=used_cols)
        self.df = self.df[list(used_cols.values())]

    def get_prefiltered_WKA(self, on_or_offshore="Windkraft an Land",
                          technology="Horizontalläufer", output=600):

        """
        Filters by the given technolgy, On/Offshore and power output.
        Translates the colums to be shorter names and more closer to usefull osm tags.

        Parameters:
        on_or_offshore: either "Windkraft an Land" or "Windkraft auf See"
        technoly: either "Horizontalläufer" or "Vertikalläufer"
        output: the nominal power output of the plant. Exclude small plants.

        Returns: Dataframe which contains the pre filtered Mastr data for
        wind power plants
        """

        # filter according to given or default values which are considered
        self.df = self.df.loc[
            (self.df["on_or_offshore"] == on_or_offshore) &
            (self.df["technology"] == technology) &
            (self.df["generator:output:electricity"] > output)]

        unit_cols = ["generator:output:electricity"]
        self.df[unit_cols] = self.df[unit_cols].astype(int)
        self.df["generator:output:electricity"] = self.df["generator:output:electricity"].astype(str) + " kW"
        return self.df

class MaStR_PV(MaStR_EEG_Base):
    def __init__(self):
        super().__init__("solar")
        # move to child class
        # rename columns to better match osm tags
        # df = df.rename(columns=used_cols)
        # df = df[list(used_cols.values())]
