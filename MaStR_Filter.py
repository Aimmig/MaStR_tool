from open_mastr import Mastr
import pandas as pd
from datetime import date
import operator

today = date.today().isoformat()


class MaStR_Filter:
    def filter_region(df, state=None, county=None, municipality=None):
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
            df = df[df["state"] == state]
        if county:
            df = df[df["county"] == county]
        if municipality:
            df = df[df["municipality"] == municipality]
        return df

    # ---- Basic filters based on NaT ------

    def get_plants_with_(df, date_type):
        """Template function to filter for plants that have
        the specified date_tye present. Also sorts data for
        convenience

        Parameter:
        date_type: Either "end_date", "start_date", "opening_date"

        Returns:
        Sorted dataframe with plants with selected date_type present
        """
        return df[df[date_type].notnull()]

    def get_plants_with_end_date(df):
        """Return only plants with known end_date.
        (Planed) Decommissioning can be safely assumed.
        This date can safely be assumed to be in the past.
        """
        return MaStR_Filter.get_plants_with_(df, "end_date")

    def get_plants_with_start_date(df):
        """Return only plants with known start_date.
        This date can safely be assumed to be in the past.
        Note this includes plant that already out of operation again.
        """
        return MaStR_Filter.get_plants_with_(df, "start_date")

    def get_plants_with_opening_date(df, comp=None, date=today):
        """Return only plants with known opening_date.
        Note this might include plants which should have openend,
        but still are not in operation.

        Parameters:
        comp: Optionally comparison parameter to filter
        date: Optionally the date to compare with
        """
        if comp:
            return df[comp(df["opening_date"], date)]
        else:
            return MaStR_Filter.get_plants_with_(df, "opening_date")

    # ---- Basic filters based on comparison with todays date -----

    def get_plants_with_future_opening_date(df):
        """Return only plants which are expected to open."""
        return MaStR_Filter.get_plants_with_opening_date(df, operator.gt)

    def get_plants_with_past_opening_date(df):
        """Return only plants that should have opened
        but still aren't operational.
        This could mean any form delay, or it was never built at all.
        """
        return MaStR_Filter.get_plants_with_opening_date(df, operator.lt)

    def get_plants_currently_operational(df):
        """Return only plants that are currently in operation.
        This means plants that are going to opened are excluded,
        and plants which are permanently closed.
        Note that short closures which are contained in the
        full data set are still included here, as these aren't
        relevant for this purpose.
        """
        df = df.loc[
            (df["opening_date"].isnull()) &
            (df["end_date"].isnull())].sort_values("start_date")
        return df
