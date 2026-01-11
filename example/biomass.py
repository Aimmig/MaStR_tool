import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.Constants import COMMON_COLS
from utils.PostProcessing import *

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'

    # columns with osm-translation
    cols = COMMON_COLS
    cols.update({"Nettonennleistung": "generator:output:electricity",
                 "EegMastrNummer": "ref:EEG"
                 })
    plants = Mastrdata("biomass").df
    query_string = "Nettonennleistung > 30"
    plants = plants.query(query_string)

    # TO-DO ...
    # plants = merge_nearby(plants)
    plants = plant_filter.get_KWK(plants)
    plants = plant_filter.get_plants_with_opening_date(plants)
    plants = plant_filter.get_columns(plants, cols)
    plants = plant_filter.get_renamed(plants, cols)
    print(plants)
    plants.to_csv("biomass.csv")
