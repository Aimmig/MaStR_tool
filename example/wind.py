import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.Constants import COMMON_COLS
from utils.PostProcessing import PostProcessing

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'

    # columns with osm-translation
    cols = COMMON_COLS
    cols.update({"InstallierteLeistung": "generator:output:electricity",
                 "Inbetriebnahmedatum": "start_date"
                 })
    #             "Hersteller": "manufacturer"
    #             "Typenbezeichnung": "model"
    plants = Mastrdata("wind").df
    query_string = "Bundesland == 'Rheinland-Pfalz' and InstallierteLeistung > 300 and Technologie == 'Horizontalläufer'"
    plants = plants.query(query_string)
    
    plants = plant_filter.get_plants_with_end_date(plants)

    # some more processing
    plants = PostProcessing.format_manufacturer(plants)

    # format power and rename
    plants = PostProcessing.format_power(plants, "MW")
    plants = PostProcessing.get_renamed(plants, cols)
    print(plants)
    plants.to_csv("wind.csv", index=False)
