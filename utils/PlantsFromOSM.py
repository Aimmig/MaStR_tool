import pyrosm
import pandas as pd
from utils.PostProcessing import PostProcessing
from utils.Constants import POWER, START, END, MODEL, HUB, ROTOR
from utils.Constants import MANUFACTURER, REF_EEG, REF_MASTR


def getPlantsWithinArea(area_file: str):
    osm = pyrosm.OSM(area_file)
    extra_attributes = [POWER,
                        START,
                        END,
                        MANUFACTURER,
                        MODEL,
                        ROTOR,
                        HUB,
                        REF_EEG,
                        REF_MASTR,
                        "name",
                        "description",
                        "note",
                        ]
    plants = osm.get_data_by_custom_criteria(custom_filter={
                                        "generator:source": ["wind"],
                                        "generator:method": ["wind_turbine"]},
                                        extra_attributes=extra_attributes,
                                        # Keep data matching the criteria above
                                        filter_type="keep",
                                        # Keep only nodes and ways
                                        # Don't know why, but some wind plants
                                        # are mapped around the foundation
                                        keep_nodes=True,
                                        keep_ways=True,
                                        keep_relations=False)

    # Potentially fix these cases in OSM
    # sanitize inputs from known problems
    # Convert column data types
    # Replace errors with NaN for now
    if HUB in plants.columns:
        plants[HUB] = plants[HUB].str.strip(' mM')
        plants[HUB] = plants[HUB].str.replace(',', '.')
        plants[HUB] = pd.to_numeric(
                plants[HUB],
                # errors='coerce',
                ).fillna(plants[HUB])
    if ROTOR in plants.columns:
        plants[ROTOR] = plants[ROTOR].str.strip(' mM')
        plants[ROTOR] = plants[ROTOR].str.replace(',', '.')
        plants[ROTOR] = pd.to_numeric(
                plants[ROTOR],
                # errors='coerce',
                ).fillna(plants[ROTOR])
    if START in plants.columns:
        plants[START] = pd.to_datetime(
                plants[START],
                errors='coerce',
                format="%Y-%m-%d",
            )
    if END in plants.columns:
        plants[END] = pd.to_datetime(
                plants[END],
                errors='coerce',
                format="%Y-%m-%d",
                )
    if MANUFACTURER in plants.columns:
        plants = PostProcessing.format_manufacturer(plants, MANUFACTURER)
    return plants
