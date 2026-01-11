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
                 "ArtDerWasserkraftanlage": "technology"
                 })
    # download data
    plants = Mastrdata("hydro").df

    # define query string ....
    query_string = "ArtDerWasserkraftanlage == 'Laufwasseranlage' and Bruttoleistung > 100"
    plants = plants.query(query_string)

    # apply filters
    plants = plant_filter.get_plants_with_end_date(plants)
    plants = plant_filter.get_columns(plants, cols)
    plants = plant_filter.get_renamed(plants, cols)
    print(plants)
    plants.to_csv("hydro.csv")
