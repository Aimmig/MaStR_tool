import os
from energycarrier.MaStR_WKA import MaStR_WKA
from utils.DataFilter import DataFilter as plant_filter
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    # select columns to keep with osm-translation
    cols = {"Nettonennleistung": "generator:output:electricity",
            "Gemeinde": "municipality",
            "Typenbezeichnung": "model"}
    # download data and only keep the columns
    wind = MaStR_WKA()
    # first specify some prefilters, like power output, generation method etc
    plants = plant_filter.prefilter_wind(wind.df)
    # get only some region
    plants = plant_filter.get_region(plants, state="Rheinland-Pfalz")

    print("--- Test example: Overview over wind power plants in RLP")
    print("----------------------")
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
