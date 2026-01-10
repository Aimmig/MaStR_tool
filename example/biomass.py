import os
from energycarrier.MaStR_biomass import MaStR_biomass
from utils.DataFilter import DataFilter as plant_filter
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    cols = {"Gemeinde": "municipality",
            "Nettonennleistung": "generator:output:electricity",
            "Biomasseart": "biomassType"}
    biomass = MaStR_biomass()
    plants = plant_filter.prefilter_biomass(
            biomass.df,
            gas_liquid_solid="Feste Biomasse")
    # get only some region
    plants = plant_filter.get_region(plants, state="Rheinland-Pfalz")

    print("--- Test example: Overview over wind power plants in RLP")
    print("----------------------")
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
