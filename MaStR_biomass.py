from MaStR_EEG_Base import MaStR_EEG_Base
import pandas as pd
from datetime import date

today = date.today().isoformat()


class MaStR_biomass(MaStR_EEG_Base):

    def __init__(self,  include_ref_eeg: bool = False):
        super().__init__("biomass", include_ref_eeg)

        # add technology specificy data which to rename
        self.used_cols.update({
             'Bruttoleistung': 'generator:output:electricity',
             'Technologie': 'technology',
             })
        #    'NameStromerzeugungseinheit': 'name_unit',
        #    'WindAnLandOderAufSee': 'on_or_offshore',
        #    'NameWindpark': 'name_windfarm',
        #    'Hersteller': 'manufacturer',
        #    'Typenbezeichnung': 'model',
        #    'Nabenhoehe': 'height:hub',
        #    'Rotordurchmesser': 'rotor:diameter'

        # optionally add even more data to print later
        # self.print_cols.extend(['name_windfarm', 'model', 'height:hub'])

        # rename columns to better match osm tags
        self.df = self.df.rename(columns=self.used_cols)
        self.df = self.df[list(self.used_cols.values())]

    def prefilter(self, gas_or_solid="Feste Biomasse", technology="Verbrennungsmotor", output: int = 500):

        """
        Filters by the given technology, On/Offshore and power output.
        Translates the columns to be shorter names and more closely to
        useful osm tags.

        Parameters:
        on_or_offshore: either "Windkraft an Land" or "Windkraft auf See"
        technology: either "Horizontalläufer" or "Vertikalläufer"
        output: the nominal power output of the plant. Exclude small plants.
        """

        # filter according to given or default values which are considered
        df = self.df.loc[
            (self.df["generator:output:electricity"] > output) &
            (self.df["technology"] == technology)]

        df = df.astype({"generator:output:electricity": int})
        # TO-add kW to column
        # df["generator:output:electricity"] = self.df[
        #        "generator:output:electricity"].astype(str) + " kW"
        return df
