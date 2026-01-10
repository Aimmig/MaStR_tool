from energycarrier import MaStR_EEG_Base as base
import pandas as pd
from datetime import date

today = date.today().isoformat()


class MaStR_biomass(base.MaStR_EEG_Base):

    def __init__(self):
        super().__init__("biomass")

    def prefilter(self, gas_liquid_solid="Gasförmige Biomasse",
                  technology="Verbrennungsmotor", output: int = 30):

        """
        Filters by the given technology, solid_or_gas and power output.

        Parameters:
        gas_liquid_solid: either "Flüssige Biomasse" or
        "Feste Biomasse" or "Gasförmige Biomasse"
        technology: z.b. "Verbrenunngsmotor", "Dampfmotor", etc.
        output: the nominal power output of the plant. Exclude small plants.
        """

        # filter according to given or default values which are considered
        df = self.df.query(
                "Biomasseart == @gas_liquid_solid &\
                Technologie == @technology &\
                Nettonennleistung > @output")

        df = df.astype({"Nettonennleistung": int})
        return df
