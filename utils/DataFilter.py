import pandas as pd
from datetime import date
import operator

today = date.today().isoformat()


class DataFilter:
    @staticmethod
    def get_region(df: pd.DataFrame, state: str = None,
                   county: str = None, municipality: str = None):
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
            df = df[df["Bundesland"] == state]
        if county:
            df = df[df["Landkreis"] == county]
        if municipality:
            df = df[df["Gemeinde"] == municipality]
        return df

    # ---- Basic filters based on NaT ------

    @staticmethod
    def get_with_(df: pd.DataFrame, date_type: str):
        """Template function to filter for plants that have
        the specified date_tye present. Also sorts data for
        convenience

        Parameter:
        date_type: Either "DatumEndgueltigeStilllegung",
                   "Inbetriebnahmedatum", "GeplantesInbetriebnahmedatum"

        Returns:
        Sorted dataframe with plants with selected date_type present
        """
        return df[df[date_type].notnull()]

    @staticmethod
    def get_plants_with_end_date(df: pd.DataFrame):
        """Return only plants with known end_date.
        (Planed) Decommissioning can be safely assumed.
        This date can safely be assumed to be in the past.
        """
        return DataFilter.get_with_(df, "DatumEndgueltigeStilllegung")

    @staticmethod
    def get_plants_with_start_date(df: pd.DataFrame):
        """Return only plants with known start_date.
        This date can safely be assumed to be in the past.
        Note this includes plant that already out of operation again.
        """
        return DataFilter.get_with_(df, "Inbetriebnahmedatum")

    @staticmethod
    def get_plants_with_opening_date(df: pd.DataFrame,
                                     comp: operator = None,
                                     comp_date: date = today):
        """Return only plants with known opening_date.
        Note this might include plants which should have openend,
        but still are not in operation.

        Parameters:
        comp: Optionally comparison parameter to filter
        date: Optionally the date to compare with
        """
        if comp:
            return df[comp(df["GeplantesInbetriebnahmedatum"], comp_date)]
        else:
            return DataFilter.get_with_(
                    df, "GeplantesInbetriebnahmedatum")

    # ---- Basic filters based on comparison with today's date -----

    @staticmethod
    def get_plants_with_future_opening_date(df: pd.DataFrame):
        """Return only plants which are expected to open."""
        return DataFilter.get_plants_with_opening_date(df, operator.gt)

    @staticmethod
    def get_plants_with_past_opening_date(df: pd.DataFrame):
        """Return only plants that should have opened
        but still aren't operational.
        This could mean any form delay, or it was never built at all.
        """
        return DataFilter.get_plants_with_opening_date(df, operator.lt)

    @staticmethod
    def get_plants_currently_operational(df: pd.DataFrame):
        """Return only plants that are currently in operation.
        This means plants that are going to opened are excluded,
        and plants which are permanently closed.
        Note that short closures which are contained in the
        full data set are still included here, as these aren't
        relevant for this purpose.
        """
        df = df.loc[
            (df["GeplantesInbetriebnahmedatum"].isnull()) &
            (df["DatumEndgueltigeStilllegung"].isnull())] \
            .sort_values("Inbetriebnahmedatum")
        return df

    @staticmethod
    def prefilter_wind(df: pd.DataFrame,
                       on_or_offshore: str = "Windkraft an Land",
                       technology: str = "Horizontalläufer",
                       output: int = 600):
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
        df = df.query(
                "WindAnLandOderAufSee == @on_or_offshore &\
                Technologie == @technology &\
                Nettonennleistung > @output")
        return df

    @staticmethod
    def prefilter_biomass(df: pd.DataFrame,
                          gas_liquid_solid: str = "Gasförmige Biomasse",
                          technology: str = "Verbrennungsmotor",
                          output: int = 30):
        """
        Filters by the given technology, solid_or_gas and power output.

        Parameters:
        gas_liquid_solid: either "Flüssige Biomasse" or
        "Feste Biomasse" or "Gasförmige Biomasse"
        technology: z.b. "Verbrenunngsmotor", "Dampfmotor", etc.
        output: the nominal power output of the plant. Exclude small plants.
        """

        # filter according to given or default values which are considered
        df = df.query(
                "Biomasseart == @gas_liquid_solid &\
                Technologie == @technology &\
                Nettonennleistung > @output")

        return df
