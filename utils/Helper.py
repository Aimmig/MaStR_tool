import pandas as pd
import geopandas as gpd
from utils.Constants import COMMON_COLS, SELECT_COLS, GEOMETRY_COLS
from utils.Constants import START


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


# TO-DO relax strict assumptions for later imports
def check_strict(df: pd.DataFrame, col: str) -> pd.DataFrame:
    mastr = "`" + col + "_mastr`"
    osm = "`" + col + "_osm`"
    return df.query(f"({osm} == {mastr})")


def check_date(df: pd.DataFrame, col: str, strict: bool) -> pd.DataFrame:
    mastr = col + "_mastr"
    osm = col + "_osm"
    if strict:
        return check_strict(df, col)
    return df.loc[(df[mastr].dt.month == df[osm].dt.month) & (df[mastr].dt.year == df[osm].dt.year)]

def plot(plot_args: str, cols_popup: list[str], plants: gpd.GeoDataFrame):
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
                     date_strict: bool =True):
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
        no_match = osm_vs_mastr[osm_vs_mastr["dist"].isnull()].fillna("dist")
        return no_match, cols
    # only keep result with non-zero distance. aka only good results
    osm_vs_mastr = osm_vs_mastr.query("dist > 0")
    if "date" in match_col:
        return check_date(osm_vs_mastr, match_col, strict=date_strict), cols
    # check for strict matches on specified column
    return check_strict(osm_vs_mastr, match_col), cols


def print_test_summary(dist: int, joined, mastr, osm, check_col, power):
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
