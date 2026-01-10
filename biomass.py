import os
from energycarrier.MaStR_biomass import MaStR_biomass
from utils.MaStR_Filter import MaStR_Filter as plant_filter
from test_printing import apply_and_print

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    wka = MaStR_biomass()
    plants = wka.prefilter()

    # get only some region
    plants = plant_filter.filter_region(plants, state="Rheinland-Pfalz")

    # Filter by existence of different date types
    print("--- Test example: Overview over wind power plants in RLP")
    print("----------------------")

    apply_and_print(plant_filter.get_plants_with_start_date, plants)
    apply_and_print(plant_filter.get_plants_with_opening_date, plants)
    apply_and_print(plant_filter.get_plants_with_end_date, plants)
    apply_and_print(plant_filter.get_plants_currently_operational, plants)
    apply_and_print(plant_filter.get_plants_with_future_opening_date, plants)
    apply_and_print(plant_filter.get_plants_with_past_opening_date, plants)
