from energycarrier import MaStR_EEG_Base as base
import pandas as pd
from datetime import date

today = date.today().isoformat()


class MaStR_biomass(base.MaStR_EEG_Base):

    def __init__(self,  include_ref_eeg: bool = False):
        super().__init__("biomass", include_ref_eeg)

    def prefilter(self, gas_or_solid="Feste Biomasse",
                  technology="Verbrennungsmotor", output: int = 500):

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
            (self.df["Nettonennleistung"] > output) &
            (self.df["Technologie"] == technology)]

        df = df.astype({"Nettonennleistung": int})
        return df
