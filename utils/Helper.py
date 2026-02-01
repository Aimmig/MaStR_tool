import pandas as pd
import geopandas as gpd
import numpy as np
from utils.Constants import COMMON_COLS, SELECT_COLS, GEOMETRY_COLS, MASTR_SUFFIX, OSM_SUFFIX
from utils.Constants import REF_MASTR_MASTR, REF_MASTR_OSM
from utils.Constants import START, END, REF_MASTR, HUB, ROTOR
from utils.Constants import MANUFACTURER, MODEL, POWER, REF_EEG


def get_column_dict(keep_columns: list[str], with_geometry: bool) -> dict:
    """
    Creates the dict of all columns for translation.
    Always includes COMMON_COLS
    If specified includes the geometry column
    Includes all key-value pairs matching keep_column
    """
    cols = dict(COMMON_COLS)
    if with_geometry:
        cols.update(GEOMETRY_COLS)
    if keep_columns:
        cols_to_keep = {k: SELECT_COLS[k] for k in keep_columns}
        cols.update(cols_to_keep)
    return cols


def get_cols_without_geometry(keep_columns: list[str]) -> list[str]:
    """
    Wrapper method to get all translated (values) without the geometry column
    """
    return list(get_column_dict(keep_columns, with_geometry=False).values())


def check_cols_in_dataframe(df: pd.DataFrame, columns: list[str]) -> list[str]:
    """
    Checks the columns list against df
    Returns part of columns list that is present in df
    """
    existing = []
    for c in columns:
        if c in df.columns:
            existing.append(c)
        else:
            print("[INFO] " + c + " does not exist. Ignoring column")
    return existing


def get_existing_ref_missmatch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return cases where after join the ref:mastr is unexpectedly different
    Only keep the id and refs
    """

    diff = df[~(df[REF_MASTR_OSM] == df[REF_MASTR_MASTR])]
    diff = diff[[REF_MASTR_MASTR, REF_MASTR_OSM, "id"]][diff[REF_MASTR_OSM].notnull()]
    diff["id"] = diff["id"].astype(int)
    diff[REF_MASTR_OSM] = diff[REF_MASTR_OSM].astype(str)
    diff[REF_MASTR_MASTR] = diff[REF_MASTR_MASTR].astype(str)
    return diff


def get_without_osm_ref(df: pd.DataFrame):
    """
    Return the part of df where ref:mastr is not present in osm
    """
    return df[df[REF_MASTR_OSM].isna()]


def check_strict(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Compare the col from osm and mastr in df
    based on strict equality
    Returns the matching part of df
    """
    mastr = "`" + col + "_mastr`"
    osm = "`" + col + "_osm`"
    return df.query(f"({osm} == {mastr})")


def check_date(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Compare date from osm and mastr in df
    based on whether month and year are identical
    Returns the matching part of df
    """
    mastr = col + MASTR_SUFFIX
    osm = col + OSM_SUFFIX
    return df.loc[(df[mastr].dt.month == df[osm].dt.month) &
                  (df[mastr].dt.year == df[osm].dt.year)]


def check_length(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Compare length values from osm and mastr in df
    based on whether one is in a small range around the other
    Returns the matching part of df
    """
    mastr = col + "_mastr"
    osm = col + "_osm"
    return df[df[mastr].between(np.floor(df[osm]-1), np.ceil(df[osm])+1)]


def plot(plot_args: str, cols_popup: list[str], plants: gpd.GeoDataFrame):
    """
    Plots the data based on the given arguments
    """
    main_col = None
    if plot_args:
        if plot_args == "year":
            main_col = "year"
            plants["year"] = plants[START].dt.year
        elif plot_args == "dist":
            main_col = "dist"
        else:
            if plot_args in SELECT_COLS:
                main_col = SELECT_COLS[plot_args]
            else:
                main_col = plot_args
        plotted_map = plants.explore(
            column=main_col,
            popup=cols_popup,
            )
        plotted_map.save('map.html')


def test_against_OSM(match_col: str, osm: gpd.GeoDataFrame,
                     mastr_units: gpd.GeoDataFrame, max_dist: int,
                     strict: bool = True):
    """
    Sjoins the given osm and mastr dfs
    Then checks whether the resulting rows match on the given
    column either strict or for some columns relaxed.
    """
    # set proper crs
    crs_str = "ESRI:102003"
    osm_to_join = osm.to_crs(crs_str)
    mastr_to_join = mastr_units.to_crs(crs_str)
    # spatial join with options, keep mastr geometry
    osm_vs_mastr = mastr_to_join.sjoin_nearest(
        osm_to_join,
        how='left',
        lsuffix='mastr',
        rsuffix='osm',
        max_distance=max_dist,
        distance_col="dist",
        )
    cols = list(osm_vs_mastr.columns.values).remove("geometry")
    # here only keep mismatches from sjon_nearest
    if match_col is None:
        no_match = osm_vs_mastr[osm_vs_mastr["dist"].isnull()]
        no_match["dist"] = 0
        return no_match, cols
    # only keep result with non-zero distance. aka only good results
    osm_vs_mastr = osm_vs_mastr.query("dist > 0")
    # some columns are for now only strict, so ignore flag
    if strict or match_col in [MANUFACTURER, MODEL, POWER, REF_EEG]:
        return check_strict(osm_vs_mastr, match_col), cols
    # start/end can be relaxed
    if match_col in [START, END]:
        return check_date(osm_vs_mastr, match_col), cols
    # length values can be relaxed
    if match_col in [HUB, ROTOR]:
        return check_length(osm_vs_mastr, match_col), cols


def print_test_summary(dist: int, joined, mastr, osm, check_col, power):
    """
    Print summary of the found matches
    """
    print("----OSM vs MaStR matches, also see generated map------")
    if check_col:
        settings = "----Settings: " + str(dist) + " with " + check_col
    else:
        settings = "----Settings: " + str(dist) + " only no matches---"
    if check_col == "generator:output:electricity":
        settings += " with " + power
    print(settings)
    print("Size OSM  : " + str(osm.shape[0]))
    print("Size MaStR: " + str(mastr.shape[0]))
    print("Matches   : " + str(joined.shape[0]))
    perc_osm = 100*joined.shape[0]/osm.shape[0]
    perc_mastr = 100*joined.shape[0]/mastr.shape[0]
    print("Matches   : " + str(perc_osm) + " % of OSM")
    print("Matches   : " + str(perc_mastr) + " % of MaStR")
    print("---Note: Size of MaStR and % is AFTER filtering----")
    return
