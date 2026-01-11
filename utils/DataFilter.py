import pandas as pd
from datetime import date
import operator

today = date.today().isoformat()


class DataFilter:
    @staticmethod
    def get(df: pd.DataFrame, expression) -> pd.DataFrame:
        """
        Filter data with given query

        Parameters:
        expression: The expression to query

        Returns:
        The filtered dataframe
        """
        return df.query(expression)

    @staticmethod
    def get_EEG(df) -> pd.DataFrame:
        return df[df["EegMastrNummer"].notnull()]

    @staticmethod
    def get_KWK(df) -> pd.DataFrame:
        return df[df["KwkMastrNummer"].notnull()]

    @staticmethod
    def get_onshore(df) -> pd.DataFrame:
        on_or_offshore = "Windkraft an Land"
        return DataFilter.get("WindAnLandOderAufSee == @on_or_offshore")

    @staticmethod
    def get_offshore(df) -> pd.DataFrame:
        on_or_offshore = "Windkraft auf See"
        return DataFilter.get("WindAnLandOderAufSee == @on_or_offshore")

    # ---- Basic filters based on NaT ------

    @staticmethod
    def get_with_(df: pd.DataFrame, date_type: str) -> pd.DataFrame:
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
    def get_plants_with_end_date(df: pd.DataFrame) -> pd.DataFrame:
        """Return only plants with known end_date.
        (Planed) Decommissioning can be safely assumed.
        This date can safely be assumed to be in the past.
        """
        return DataFilter.get_with_(df, "DatumEndgueltigeStilllegung")

    @staticmethod
    def get_plants_with_start_date(df: pd.DataFrame) -> pd.DataFrame:
        """Return only plants with known start_date.
        This date can safely be assumed to be in the past.
        Note this includes plant that already out of operation again.
        """
        return DataFilter.get_with_(df, "Inbetriebnahmedatum")

    @staticmethod
    def get_plants_with_opening_date(df: pd.DataFrame,
                                     comp: operator = None,
                                     comp_date: date = today) -> pd.DataFrame:
        """Return only plants with known opening_date.
        Note this might include plants which should have opened,
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
    def get_plants_with_future_opening_date(df: pd.DataFrame) -> pd.DataFrame:
        """Return only plants which are expected to open."""
        return DataFilter.get_plants_with_opening_date(df, operator.gt)

    @staticmethod
    def get_plants_with_past_opening_date(df: pd.DataFrame) -> pd.DataFrame:
        """Return only plants that should have opened
        but still aren't operational.
        This could mean any form delay, or it was never built at all.
        """
        return DataFilter.get_plants_with_opening_date(df, operator.lt)

    @staticmethod
    def get_plants_currently_operational(df: pd.DataFrame) -> pd.DataFrame:
        """Return only plants that are currently in operation.
        This means plants that are going to open are excluded,
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
    def get_columns(df: pd.DataFrame, cols: dict) -> pd.DataFrame:
        return df[list(cols.keys())]
