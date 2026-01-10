from open_mastr import Mastr
import pandas as pd
from datetime import date
import operator

today = date.today().isoformat()


class MaStR_Filter:
    @staticmethod
    def filter_region(df: pd.DataFrame, state: str = None,
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
        return MaStR_Filter.get_with_(df, "DatumEndgueltigeStilllegung")

    @staticmethod
    def get_plants_with_start_date(df: pd.DataFrame):
        """Return only plants with known start_date.
        This date can safely be assumed to be in the past.
        Note this includes plant that already out of operation again.
        """
        return MaStR_Filter.get_with_(df, "Inbetriebnahmedatum")

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
            return MaStR_Filter.get_with_(df,
                                          "GeplantesInbetriebnahmedatum")

    # ---- Basic filters based on comparison with today's date -----

    @staticmethod
    def get_plants_with_future_opening_date(df: pd.DataFrame):
        """Return only plants which are expected to open."""
        return MaStR_Filter.get_plants_with_opening_date(df, operator.gt)

    @staticmethod
    def get_plants_with_past_opening_date(df: pd.DataFrame):
        """Return only plants that should have opened
        but still aren't operational.
        This could mean any form delay, or it was never built at all.
        """
        return MaStR_Filter.get_plants_with_opening_date(df, operator.lt)

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
