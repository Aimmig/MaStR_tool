from utils.Mastrdata import download
from utils.PreConfiguredParser import createSimpleMastrQueryParser
from utils.SearchByMastrRef import search_ref
from dotenv import load_dotenv


def get_data_selection(source: str, refs: list[str], keepColumns: list[str]):
    """
    Wrapper function that gets the data.
    Keeps only the specified refs and columns.
    Returns: The pandas DataFrame
    """
    plants = download(source)
    plants, ref_col = search_ref(plants, refs)
    return plants, keepColumns + [ref_col]


def get_data(source: str, refs: list[str], keepColumns: list[str]):
    """
    Returns the MaStR data selection
    """
    mastr_units, cols = get_data_selection(source, refs, keepColumns)
    return mastr_units[cols]


if __name__ == "__main__":
    env_file = "env_conf/.get_by_ref_env"
    load_dotenv(env_file)
    parser = createSimpleMastrQueryParser()
    arguments = parser.parse_args()
    source = arguments.source
    refs = arguments.ref
    keepColumns = arguments.keepColumns
    df = get_data(source, refs, keepColumns)
    csv = df.to_csv(None,
                    index=False,
                    )
    if csv:
        print(csv)
