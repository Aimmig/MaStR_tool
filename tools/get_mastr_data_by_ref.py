import os
from utils.Mastrdata import download
from utils.PreConfiguredParser import createSimpleMastrQueryParser
from utils.SearchByMastrRef import search_ref
from dotenv import load_dotenv


def get_data_selection(args):
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    plants = download(args.source)
    refs = args.ref
    plants, ref_col = search_ref(plants, refs)
    return plants, args.keepColumns + [ref_col]


if __name__ == "__main__":
    load_dotenv("env_conf/.get_by_ref_env")
    parser = createSimpleMastrQueryParser()
    arguments = parser.parse_args()
    mastr_units, cols = get_data_selection(arguments)
    csv = mastr_units[cols].to_csv(
                None,
                index=False,
                )
    if csv:
        print(csv)
