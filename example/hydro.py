import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.DataFilter import COMMON_COLS
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    # select columns to keep with osm-translation
    cols = COMMON_COLS
    cols.update({"Nettonennleistung": "generator:output:electricity",
                 "Gemeinde": "municipality",
                 "ArtDerWasserkraftanlage": "technology"
                 })
    # download data and only keep the columns
    plants = Mastrdata("hydro").df

    # define query string ....
    query_string = "ArtDerWasserkraftanlage == 'Laufwasseranlage' and Bruttoleistung > 100"
    plants = plants.query(query_string)

    # Filter by existence of different date types
    apply_and_print(plant_filter.get_plants_with_start_date,
                    plants, cols)
