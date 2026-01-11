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
                 "Gemeinde": "municipality",
                 "Technologie": "technology"
                 })
    plants = Mastrdata("gsgk").df
    query_string = "Technologie == 'Verbrennungsmotor' and Energietraeger == 'Klärschlamm'"
    plants = plants.query(query_string)

    plants = PlantFilter.get_KWK(plants)
    plants =PlantFilter.get_plants_currently_operational(plants)

    # format power and rename
    plants = PostProcessing.format_power(plants, "MW")
    plants = PostProcessing.get_renamed(plants, cols)
    print(plants)
    plants.to_csv("gsgk.csv")
