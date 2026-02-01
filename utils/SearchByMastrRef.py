from utils.Constants import MASTR_REFS
import geopandas as gpd


def determine_key(ref: list[str]):
    """
    Determines which short-hand key for ref should be used.
    Matches length and start of different MaStR ref keys.
    All ref in list should be from same sort.

    Returns: The key or None if not all are matching.
    """
    key = None
    ref_len = 0
    if len(set(map(len, ref))) == 1:
        ref_len = len(ref[0])
    # 3 char refs have all length 15
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
    # Exxx is 33 length
    if ref_len == 33:
        if all(item.startswith('E') for item in ref):
            key = 'E'
    # Axxxx is 14 length
    if ref_len == 14:
        if all(item.startswith('A') for item in ref):
            key = 'E'
    return key


def search_ref(mastr: gpd.GeoDataFrame, ref: list[str]):
    """
    Searches the dataframe for all matches with the given
    ref list

    Returns: The matching part of dataframe and the name
             of the matching ref column
    """
    key = determine_key(ref)
    if key:
        df = mastr[mastr[MASTR_REFS[key]].isin(ref)]
        return df, MASTR_REFS[key]
    return None
