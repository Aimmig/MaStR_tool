import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.DataFilter import COMMON_COLS
from utils.PostProcessing import *
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage

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

    # Filter by existence of different date types
    apply_and_print(plant_filter.get_plants_with_start_date,
                    plants, cols)
