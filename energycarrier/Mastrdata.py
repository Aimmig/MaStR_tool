from open_mastr import Mastr
import pandas as pd
from datetime import date
import operator

today = date.today().isoformat()


class Mastrdata:

    def __init__(self, energy_carrier: str):

        """
        Downloads the Mastr unit data and filters for the given technology.
        Large parts of data is thrown away since it's not really relevant,
        also throws away lots of empty columns which are empty.

        Parameters:
        energy_carrier: The energy carrier to download
        """

        # download relevant data with api
        db = Mastr()
        db.download(data=energy_carrier, api_data_types=["unit_data"],
                    api_location_type=["location_elec_generation"])
        # get the required tables
        table = energy_carrier + "_extended"
        df_extended = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
        df_extended = pd.read_sql(sql=table, con=db.engine)

        table = energy_carrier + "_eeg"
        df_eeg = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            con=db.engine)
        df_eeg = pd.read_sql(sql=table, con=db.engine)

        # join on the internally used key
        key = 'EegMastrNummer'
        # join and remove some duplicate columns which
        df = df_extended.merge(df_eeg, on=key, how='left',
                               suffixes=('', '_DROP')).filter(
                                       regex='^(?!.*_DROP)')

        # filter data before further processing
        self.df = df.dropna(axis=1, how='all')
