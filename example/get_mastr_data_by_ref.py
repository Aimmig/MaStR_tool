import argparse
import os
from energycarrier.Mastrdata import Mastrdata
from utils.PreConfiguredParser import createSimpleMastrQueryParser
from utils.Helper import get_cols_without_geometry
from utils.Helper import check_cols_in_dataframe
from utils.PostProcessing import PostProcessing
from utils.Constants import MASTR_REFS
import geopandas as gpd


def searchref(mastr: gpd.GeoDataFrame, ref: list[str]):
    key = None
    ref_len = 0
    if len(set(map(len, ref))) == 1:
        ref_len = len(ref[0])
    if ref_len == 15:
        if all(item.startswith('SEE') for item in ref):
            key = 'SEE'
        if all(item.startswith('SEL') for item in ref):
            key = 'SEL'
        if all(item.startswith('SGE') for item in ref):
            key = 'SGE'
        if all(item.startswith('EEG') for item in ref):
            key = 'EEG'
        if all(item.startswith('ABR') for item in ref):
            key = 'ABR'
        if all(item.startswith('KWK') for item in ref):
            key = 'KWK'
    if ref_len == 33:
        if all(item.startswith('E') for item in ref):
            key = 'E'
    if ref_len == 14:
        if all(item.startswith('A') for item in ref):
            key = 'E'
    if key:
        df = mastr[mastr[MASTR_REFS[key]].isin(ref)]
        return df, MASTR_REFS[key]
    return None


def getData(args) -> gpd.GeoDataFrame:
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    plants = Mastrdata(args.source).df

    refs = args.ref
    plants, ref_col = searchref(plants, refs)

    # cols_to_keep = check_cols_in_dataframe(plants, args.keepColumns)
    # plants = PostProcessing.translate(plants, cols_to_keep)
    return plants, args.keepColumns + [ref_col]

    if key:
        df = mastr[mastr[MASTR_REFS[key]].isin(ref)]
        return df, MASTR_REFS[key]
    return None


def getData(args) -> gpd.GeoDataFrame:
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    plants = Mastrdata(args.source).df

    refs = args.ref
    plants, ref_col = searchref(plants, refs)

    # cols_to_keep = check_cols_in_dataframe(plants, args.keepColumns)
    # plants = PostProcessing.translate(plants, cols_to_keep)
    return plants, args.keepColumns + [ref_col]


if __name__ == "__main__":
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    parser = createSimpleMastrQueryParser()
    arguments = parser.parse_args()
    mastr_units, cols = getData(arguments)
    csv = mastr_units[cols].to_csv(
                arguments.output,
                index=False,
                )
    if csv:
        print(csv)
