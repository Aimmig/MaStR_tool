import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    # select columns to keep with osm-translation
    cols = {"Nettonennleistung": "generator:output:electricity",
            "Gemeinde": "municipality",
            "ArtDerWasserkraftanlage": "technology"}
    # download data and only keep the columns
    plants = Mastrdata("hydro").df
    
    # Filter by existence of different date types
    apply_and_print(plant_filter.get_plants_with_start_date,
                    plants)
    apply_and_print(plant_filter.get_plants_with_opening_date,
                    plants)
    apply_and_print(plant_filter.get_plants_with_end_date,
                    plants)
    apply_and_print(plant_filter.get_plants_currently_operational,
                    plants)
    apply_and_print(plant_filter.get_plants_with_future_opening_date,
                    plants)
    apply_and_print(plant_filter.get_plants_with_past_opening_date,
                    plants, cols)
