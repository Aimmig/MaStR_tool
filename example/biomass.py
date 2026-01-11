import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as PlantFilter
from utils.Constants import COMMON_COLS
from utils.PostProcessing import PostProcessing

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
    plants = PlantFilter.get_KWK(plants)
    plants = PlantFilter.get_plants_with_opening_date(plants)

    # format power and rename
    plants = PostProcessing.format_power(plants, "MW")
    plants = PostProcessing.get_renamed(plants, cols)

    print(plants)
    plants.to_csv("biomass.csv")
