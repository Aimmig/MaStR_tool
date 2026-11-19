from utils.PreConfiguredParser import createOSMLifecycleParser
from utils.PlantsFromOSM import getWindPlantsInArea
from dotenv import load_dotenv
from get_mastr_data_by_ref import get_data
from utils.Constants import REF_MASTR
from utils.Constants import START, END
from utils.Constants import MANUFACTURER
from utils.Constants import CONSTRUCTION_POWER, PLANNED_POWER
from utils.Helper import plot
import pandas as pd
import geopandas

DESC_CONSTR = "under construction"
GEN = "generator"
DESC = "description"


def fix_refs(refs: list[str]):
    """
    Fixes the list of refs by dropping all elements
    which are unexpected in this context
    """
    return [r for r in refs if len(r) == 15 and r.startswith("SEE")]


def filter_construction_or_planned(df: pd.DataFrame):
    """
    Filter dataframe where units are considered
    as under construction/planned etc
    """
    col_set = set(df.columns)
    if {CONSTRUCTION_POWER, PLANNED_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (DESC_CONSTR in df[DESC]) | (df[PLANNED_POWER] == GEN)]
    if {CONSTRUCTION_POWER, DESC} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN) | (DESC_CONSTR in df[DESC])]
    if {CONSTRUCTION_POWER} <= col_set:
        return df.loc[(df[CONSTRUCTION_POWER] == GEN)]


def get_construction_refs_osm(df: pd.DataFrame):
    """
    Filters for units which are considered as
    tagged construction and ref:mastr exists
    """
    tags = filter_construction_or_planned(df)
    return tags[REF_MASTR].dropna().to_list()


def get_active_refs_osm(df: pd.DataFrame):
    """
    Filters for units which are considered operational
    and ref:mastr exists
    """
    tags = df.loc[(df["power"] == GEN)]
    return tags[REF_MASTR].dropna().to_list()


def get_and_read_mastr(refs: list[str], cols: list[str]):
    """
    Gets the MaStR data for the refs
    """
    fixed_refs = fix_refs(refs)
    return get_data("wind", fixed_refs, cols)


def get_osm_potentially_open(area: str, keepCols: list[str]):
    """
    Gets all osm wind units in area which are considered as
    tagged construction
    If possible gets MaStR-Data for these units.
    Returns units where construction has already finished.
    """
    osm_units = getWindPlantsInArea(area, sanitize=True)
    constr_refs = get_construction_refs_osm(osm_units)
    cols = ["Inbetriebnahmedatum", "Laengengrad", "Breitengrad"]
    cols = cols + keepCols
    maybe_open = get_and_read_mastr(constr_refs, cols)
    return maybe_open.dropna(subset=["Inbetriebnahmedatum"])


def get_osm_potentially_closed(area: str, keepCols: list[str]):
    """
    Gets all osm wind units in area which are considered as
    currently operational.
    If possible gets MaStR-Data for these units.
    Returns units which have been permanently shut down.
    """
    osm_units = getWindPlantsInArea(area, sanitize=True)
    active_refs = get_active_refs_osm(osm_units)
    cols = ["DatumEndgueltigeStilllegung", "Laengengrad", "Breitengrad"]
    cols = cols + keepCols
    active = get_and_read_mastr(active_refs, cols)
    return active.dropna(subset=["DatumEndgueltigeStilllegung"])


def get_by_life_cycle(env_file: str, life_cycle: str):
    """
    Get units for specified lifecyle
    """
    load_dotenv(env_file)
    parser = createOSMLifecycleParser()
    args = parser.parse_args()
    if life_cycle == "construction":
        res = get_osm_potentially_open(args.area, args.keepColumns)
    if life_cycle == "disused":
        res = get_osm_potentially_closed(args.area, args.keepColumns)
    res = rename_cols_before_plot(res)
    print(res)
    gdf = geopandas.GeoDataFrame(
    res, geometry=geopandas.points_from_xy(res.Laengengrad, res.Breitengrad), crs="EPSG:4326")
    plot(args.plot, [], gdf)


def rename_cols_before_plot(df):
    df.rename(columns={"Inbetriebnahmedatum": START}, inplace=True)
    df.rename(columns={"Hersteller": MANUFACTURER}, inplace=True)
    df.rename(columns={"DatumEndgueltigeStilllegung": END}, inplace=True)
    return df
