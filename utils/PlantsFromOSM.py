import pyrosm
import osmium
import pandas as pd
import os.path
from utils.PostProcessing import PostProcessing
from utils.Constants import POWER, START, END, MODEL, HUB, ROTOR
from utils.Constants import MANUFACTURER, REF_EEG, REF_MASTR


def filter_and_write(osm_pbf_in: str, tmp_file: str,
                     invalidate_cache: bool = False):
    """
    Filters the osm pbf for useful tags and writes output
    to tmp file. This tmp file should be used after that.
    """
    if invalidate_cache or not os.path.isfile(tmp_file):
        gen_tag_filter = osmium.filter.TagFilter(
                ("generator:source", "wind"),
                ("generator:method", "wind_turbine"))
        fp = osmium.FileProcessor(osm_pbf_in).with_filter(
                osmium.filter.EmptyTagFilter()).with_filter(gen_tag_filter)
        with osmium.BackReferenceWriter(tmp_file,
                                        ref_src=osm_pbf_in,
                                        overwrite=True) as writer:
            for obj in fp:
                writer.add(obj)


def getPlantsWithinArea(area_file: str, gen_source: str, gen_method: str,
                        sanitize: bool, date_format: str = "%Y-%m-%d"):
    """
    Extracts the ways/nodes with given method/source from
    given osm pbf area file (Should be pre-filtered).
    Applies some basic type conversion, like date, int etc.
    Optionaly sanitzes some of the inputs.
    Returns gpd containing the data
    """
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
                        "ref",
                        "name",
                        "description",
                        "note",
                        ]
    plants = osm.get_data_by_custom_criteria(custom_filter={
                                        "generator:source": [gen_source],
                                        "generator:method": [gen_method]},
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
        if sanitize:
            plants[HUB] = plants[HUB].str.strip(' mM')
            plants[HUB] = plants[HUB].str.replace(',', '.')
            plants[HUB] = pd.to_numeric(
                    plants[HUB],
                    )  # .fillna(plants[HUB])
        else:
            plants[HUB] = pd.to_numeric(
                    plants[HUB],
                    errors='coerce',
                    ).fillna(plants[HUB])

    if ROTOR in plants.columns:
        if sanitize:
            plants[ROTOR] = plants[ROTOR].str.strip(' mM')
            plants[ROTOR] = plants[ROTOR].str.replace(',', '.')
            plants[ROTOR] = pd.to_numeric(
                    plants[ROTOR],
                    )  # .fillna(plants[ROTOR])
        else:
            plants[ROTOR] = pd.to_numeric(
                    plants[ROTOR],
                    errors='coerce',
                    ).fillna(plants[ROTOR])
    if START in plants.columns:
        plants[START] = pd.to_datetime(
                plants[START],
                errors='coerce',
                format=date_format,
            )
    if END in plants.columns:
        plants[END] = pd.to_datetime(
                plants[END],
                errors='coerce',
                format=date_format,
                )
    if MANUFACTURER in plants.columns:
        plants = PostProcessing.format_manufacturer(plants, MANUFACTURER)
    # sanitze model from some often used chars
    if MODEL in plants.columns:
        if sanitize:
            plants[MODEL] = plants[MODEL].str.replace(
                    r'[ .,-\/]', '', regex=True)
    return plants
