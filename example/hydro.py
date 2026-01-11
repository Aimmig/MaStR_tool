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
                 "ArtDerWasserkraftanlage": "technology"
                 })
    plants = Mastrdata("hydro").df
    query_string = "ArtDerWasserkraftanlage == 'Laufwasseranlage' and Bruttoleistung > 100"
    plants = plants.query(query_string)

    plants = PlantFilter.get_plants_with_end_date(plants)

    plants = PostProcessing.format_power(plants, "kW")
    plants = PostProcessing.get_renamed(plants, cols)
    print(plants)
    plants.to_csv("hydro.csv")
