import os
from MaStR_biomass import MaStR_biomass
from MaStR_Filter import MaStR_Filter as plant_filter

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    # Small test example to show usage
    bio = MaStR_biomass(include_ref_eeg=True)
    plants = bio.prefilter()

    # get only some region
    plants = plant_filter.filter_region(plants, state="Rheinland-Pfalz")

    # Filter by existence of different date types
    print("--- Test example: Overview over wind power plants in RLP")
    print("----------------------")

    df = plant_filter.get_plants_with_start_date(plants)
    print("Plants that have ever openend, including already closed ones")
    print(df[cols])
    print("----------------------")

    df = plant_filter.get_plants_with_opening_date(plants)
    print("Plants with start date including some with past start date")
    print(df[cols])
    print("----------------------")

    df = plant_filter.get_plants_with_end_date(plants)
    print("Plants that are shutdown permanentyl")
    print(df[cols])
    print("----------------------")

    df = plant_filter.get_plants_currently_operational(plants)
    print("Plants currentyl in operation")
    print(df[cols])
    print("----------------------")

    df = plant_filter.get_plants_with_future_opening_date(plants)
    print("Plants expected to open in the future")
    print(df[cols])
    print("----------------------")

    df = plant_filter.get_plants_with_past_opening_date(plants)
    print("Plants that haven't started but were expected to start already")
    print(df[cols])
    print("----------------------")
