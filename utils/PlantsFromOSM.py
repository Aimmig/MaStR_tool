import pyrosm
import pandas as pd


def getPlantsWithinArea(area_file: str):
    osm = pyrosm.OSM(area_file)
    extra_attributes = ["generator:output:electricity",
                        "start_date",
                        "end_date",
                        "manufacturer",
                        "model",
                        "rotor:diameter",
                        "height:hub",
                        "ref:eeg",
                        "ref:MaStR",
                        ]
    plants = osm.get_data_by_custom_criteria(custom_filter={
                                        "generator:source": ["wind"],
                                        "generator:method": ["wind_turbine"]},
                                        extra_attributes=extra_attributes,
                                        # Keep data matching the criteria above
                                        filter_type="keep",
                                        # Keep only nodes and ways
                                        # Don't know why, but someone mapped
                                        # wind plants as ways around the foundation
                                        keep_nodes=True,
                                        keep_ways=True,
                                        keep_relations=False)
    # Convert column data types
    # Replace errors with NaN for now
    # Potentially fix these cases in OSM
    plants["height:hub"] = pd.to_numeric(
            plants["height:hub"],
            errors='coerce',
            )
    plants["rotor:diameter"] = pd.to_numeric(
            plants["rotor:diameter"],
            errors='coerce',
            )
    plants["start_date"] = pd.to_datetime(
            plants["start_date"],
            errors='coerce',
            format="%Y-%m-%d",
            )
    plants["end_date"] = pd.to_datetime(
            plants["end_date"],
            errors='coerce',
            format="%Y-%m-%d",
            )
    return plants
