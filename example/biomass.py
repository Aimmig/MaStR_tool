import os
from energycarrier.Mastrdata import Mastrdata
from utils.DataFilter import DataFilter as plant_filter
from utils.DataFilter import COMMON_COLS
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage

    cols = COMMON_COLS
    cols.update({"Gemeinde": "municipality",
                 "Nettonennleistung": "generator:output:electricity",
                 "Biomasseart": "biomassType"
                 })
    plants = Mastrdata("biomass").df
    query_string = "Bundesland == 'Bayern' and Biomasseart == 'Feste Biomasse' and Technologie ==  'Dampfmotor'"
    plants = plants.query(query_string)
    plants = plant_filter.get_KWK(plants)

    # Filter by existence of different date types and only print columns
    apply_and_print(plant_filter.get_plants_with_start_date,
                    plants, cols)
    apply_and_print(plant_filter.get_plants_with_opening_date,
                    plants, cols)
    apply_and_print(plant_filter.get_plants_with_end_date,
                    plants, cols)
    apply_and_print(plant_filter.get_plants_currently_operational,
                    plants, cols)
    apply_and_print(plant_filter.get_plants_with_future_opening_date,
                    plants, cols)
    apply_and_print(plant_filter.get_plants_with_past_opening_date,
                    plants, cols)
