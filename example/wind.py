import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.Constants import COMMON_COLS
from utils.PostProcessing import *
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    # select columns to keep with osm-translation
    cols = COMMON_COLS
    cols.update({"InstallierteLeistung": "generator:output:electricity",
                 "Inbetriebnahmedatum": "start_date"
                 })
    #             "Hersteller": "manufacturer"
    #             "Typenbezeichnung": "model"
    # download data and only keep the columns
    plants = Mastrdata("wind").df

    # custom query ..
    query_string = "Bundesland == 'Rheinland-Pfalz' and InstallierteLeistung > 300 and Technologie == 'Horizontalläufer'"
    plants = plants.query(query_string)

    plants = format_power(plants, "kW")
    plants = format_manufacturer(plants)

    print("--- Test example: Overview over wind power plants in RLP")
    print("----------------------")
    apply_and_print(plant_filter.get_plants_with_end_date,
                    plants, cols, "with_end_date_rlp.csv")
