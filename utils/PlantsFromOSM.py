import pyrosm
import osmium
import pandas as pd
import os.path
from utils.PostProcessing import PostProcessing
from utils.Constants import POWER, START, END, MODEL, HUB, ROTOR
from utils.Constants import MANUFACTURER, REF_EEG, REF_MASTR
from utils.Constants import OTHER_OSM, PREFIX_POWER


def get_fixed_area_fps(area: str):
    # Fix cases where _ in selectable regions
    # is replaced with - in downloaded file name
    area = area.replace("_", "-")
    # Capitalize cities which are states
    if area in ["berlin", "hamburg", "bremen"]:
        area = area.title()
    # assemble file paths
    if not os.getenv("OSM_TMP_PATH").endswith('/'):
        fp_path = os.getenv("OSM_TMP_PATH") + '/'
    else:
        fp_path = os.getenv("OSM_TMP_PATH")
    fp_base = fp_path + area
    suffix = ".osm.pbf"
    fp_full = fp_base + "-latest" + suffix
    fp_filtered = fp_base + "-latest-filtered" + suffix
    # cities which are states don't have "latest"
    if area in ["Berlin", "Hamburg", "Bremen"]:
        fp_full = fp_full.replace("-latest", "")
        fp_filtered = fp_filtered.replace("-latest", "")
    return fp_full, fp_filtered


def getWindPlantsInArea(area: str, sanitize: bool):
    return getPlantsWithinArea(area, "wind", "wind_turbine", sanitize)


def getPlantsWithinArea(area: str, gen_source: str, gen_method: str,
                        sanitize: bool = False):
    """
    Wrapper function to download, pre-filter and then read and prepare
    data from osm pbf
    """
    fp_full, fp_filtered = get_fixed_area_fps(area)
    if not os.path.isfile(fp_full):
        # ???
        fp = pyrosm.get_data(area, update=True)
    else:
        print("[INFO]: Using existing base file " + fp_full)
    filter_and_write(fp_full, fp_filtered,
                     gen_source, gen_method)
    return read_and_prepare(fp_filtered, gen_source, gen_method,
                            sanitize=sanitize)


def filter_and_write(osm_pbf_in: str, tmp_file: str, gen_source: str, gen_method: str):
    """
    Filters the osm pbf for useful tags and writes output
    to tmp file. This tmp file should be used after that.
    """
    if not os.path.isfile(tmp_file):
        print("[INFO]: Recreating filtered file " + tmp_file)
        gen_tag_filter = osmium.filter.TagFilter(
                ("generator:source", gen_source),
                ("generator:method", gen_method))
        fp = osmium.FileProcessor(osm_pbf_in).with_filter(
                osmium.filter.EmptyTagFilter()).with_filter(gen_tag_filter)
        with osmium.BackReferenceWriter(tmp_file,
                                        ref_src=osm_pbf_in,
                                        overwrite=True) as writer:
            # caution this can make problems when no further data on node
            # aka no further useful tags exists
            # maybe fix here or fix when preparing/sanitizing pandas df
            for obj in fp:
                writer.add(obj)
    else:
        print("[INFO]: Using existing filtered file " + tmp_file)


def read_and_prepare(file: str, gen_source: str, gen_method: str,
                     sanitize: bool):
    """
    Extracts the ways/nodes with given method/source from
    given osm pbf area file (Should be pre-filtered).
    Applies some basic type conversion, like date, int etc.
    Optionally sanitizes some of the inputs.
    Returns gpd containing the data
    """
    osm = pyrosm.OSM(file)
    extra_attributes = [POWER,
                        START,
                        END,
                        MANUFACTURER,
                        MODEL,
                        ROTOR,
                        HUB,
                        REF_EEG,
                        REF_MASTR] + OTHER_OSM + PREFIX_POWER
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
    return prepare(plants, sanitize)


def prepare(plants: pd.DataFrame, sanitize: bool):
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
    date_format = os.getenv("DATE_FORMAT")
    if not date_format:
        date_format = "%Y-%m-%d"
    if START in plants.columns:
        # copy raw date for checking str later
        plants[START + "_raw"] = plants[START]
        plants = plants.copy()
        plants[START] = pd.to_datetime(
                plants[START],
                errors='coerce',
                format=date_format,
            )
    if END in plants.columns:
        # copy raw date for checking str later
        plants[END + "_raw"] = plants[END]
        plants = plants.copy()
        plants[END] = pd.to_datetime(
                plants[END],
                errors='coerce',
                format=date_format,
                )
    if MANUFACTURER in plants.columns:
        # plants[[MANUFACTURER, "id"]].to_csv("bla.csv", index=False)
        plants = PostProcessing.format_manufacturer(plants, MANUFACTURER)
    # sanitize model from some often used chars
    if MODEL in plants.columns:
        if sanitize:
            plants[MODEL] = plants[MODEL].str.replace(
                    r'[ .,-\/]', '', regex=True)
    return plants
