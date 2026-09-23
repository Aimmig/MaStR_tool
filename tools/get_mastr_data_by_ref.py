from utils.Mastrdata import download
from utils.PreConfiguredParser import createSimpleMastrQueryParser
from utils.SearchByMastrRef import search_ref
from dotenv import load_dotenv


def get_data_selection(source, refs, keepColumns):
    """
    Wrapper function that gets the data and applies the parser args.
    Returns: The pandas DataFrame
    """
    plants = download(source)
    plants, ref_col = search_ref(plants, refs)
    return plants, keepColumns + [ref_col]


def get_data(source, refs, keepColumns):
    mastr_units, cols = get_data_selection(source, refs, keepColumns)
    csv = mastr_units[cols].to_csv(
                None,
                index=False,
                )
    return csv


if __name__ == "__main__":
    env_file = "env_conf/.get_by_ref_env"
    load_dotenv(env_file)
    parser = createSimpleMastrQueryParser()
    arguments = parser.parse_args()
    source = arguments.source
    refs = arguments.ref
    keepColumns = arguments.keepColumns
    csv = get_data(source, refs, keepColumns)
    if csv:
        print(csv)
