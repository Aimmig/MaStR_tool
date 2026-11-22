from utils.Mastrdata import get_filtered_mastr_from_args
from utils.Helper import plot, test_against_OSM
from utils.Helper import get_existing_ref_missmatch
from utils.Helper import get_without_osm_ref
from utils.PlantsFromOSM import getWindPlantsInArea
from utils.Constants import SELECT_COLS, LON, LAT
from utils.Constants import REF_MASTR_MASTR, MASTR_SUFFIX, OSM_SUFFIX
import pandas as pd


def drop_units_where_ref_mastr_osm_exists(df, osm_pbf, drop_or_keep="all"):
    if drop_or_keep == "all":
        return df
    osm_units = getWindPlantsInArea(osm_pbf, sanitize=True)
    ref_mastr_osm = osm_units.dropna(subset=["ref:mastr"])["ref:mastr"]
    keep = pd.merge(right=ref_mastr_osm, left=df, how='inner', right_on="ref:mastr", left_on="ref:mastr_mastr")
    if drop_or_keep == "keep":
        return keep
    if drop_or_keep == "drop":
        return df[~df['ref:mastr_mastr'].isin(keep['ref:mastr_mastr'])]
    return df


def keep_only_with_generator_tag(df, which: str):
    if which == "all":
        return df
    if which == "generator":
        return df.loc[df['power'] == "generator"]
    if which == "construction":
        return df.loc[df['construction:power'] == "generator"]
    if which == "prosed":
        return df.loc[df['proposed:power'] == "generator"]
    return df


def compute_matches(arguments, distance, drop_or_keep="all", keep_only_power="all"):
    mastr_units, cols = get_filtered_mastr_from_args(arguments)
    csv = mastr_units[cols].to_csv(
                None,
                index=False,
                )
    if arguments.testagainstOSM:
        osm_pbf = arguments.testagainstOSM
        if arguments.keepColumns is not None and len(arguments.keepColumns) != 1:
            raise ValueError("Only exactly one colum with testosm")
        if arguments.keepColumns is None:
            check_col = None
        else:
            check_col = "".join(arguments.keepColumns)
            check_col = SELECT_COLS[check_col]
        osm_units = getWindPlantsInArea(osm_pbf,
                                        sanitize=True)
        joined, cols = test_against_OSM(check_col, osm_units,
                                        mastr_units, max_dist=distance,
                                        strict=True)
        if arguments.keepColumns is None:
            joined = drop_units_where_ref_mastr_osm_exists(joined, osm_pbf, drop_or_keep=drop_or_keep)
            joined = keep_only_with_generator_tag(joined, keep_only_power)
            plot("dist", cols, joined)
            exit

        joined = keep_only_with_generator_tag(joined, keep_only_power)
        plot("dist", cols, joined)
        mastr_diff = get_existing_ref_missmatch(joined)
        joined = get_without_osm_ref(joined)
        if REF_MASTR_MASTR in list(joined.columns.values):
            mastr_col_sel = [LAT+MASTR_SUFFIX, LON+MASTR_SUFFIX, REF_MASTR_MASTR]
        else:
            mastr_col_sel = [LAT+MASTR_SUFFIX, LON+MASTR_SUFFIX]
        if check_col:
            mastr_col_sel += [check_col+MASTR_SUFFIX, check_col+OSM_SUFFIX, "id"]
        try:
            joined['id'] = joined['id'].astype(int)
        except pd.errors.IntCastingNaNError:
            pass
        csv = joined[mastr_col_sel].to_csv(None, index=False)
        if csv:
            print(csv)
