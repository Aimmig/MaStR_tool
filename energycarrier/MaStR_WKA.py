from energycarrier import MaStR_EEG_Base as base
import pandas as pd
from datetime import date

today = date.today().isoformat()


class MaStR_WKA(base.MaStR_EEG_Base):

    def __init__(self):
        super().__init__("wind")

    def prefilter(self, on_or_offshore: str = "Windkraft an Land",
                  technology: str = "Horizontalläufer", output: int = 600):

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
            (self.df["WindAnLandOderAufSee"] == on_or_offshore) &
            (self.df["Technologie"] == technology) &
            (self.df["Nettonennleistung"] > output)]

        df = df.astype({"Nettonennleistung": int})
        return df
