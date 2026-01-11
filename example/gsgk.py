import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.Constants import COMMON_COLS

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'

    # columns with osm-translation
    cols = COMMON_COLS
    cols.update({"Nettonennleistung": "generator:output:electricity",
                 "Gemeinde": "municipality",
                 "Technologie": "technology"
                 })
    # download data
    plants = Mastrdata("gsgk").df

    # write custom query string like this
    query_string = "Technologie == 'Verbrennungsmotor' and Energietraeger == 'Klärschlamm'"
    plants = plant_filter.get(plants, query_string)
    plants = plant_filter.get_KWK(plants)
    plants = plant_filter.get_plants_currently_operational(plants)
    plants = plant_filter.get_columns(plants, cols)
    plants = plant_filter.get_renamed(plants, cols)
    print(plants)
    plants.to_csv("gsgk.csv")
