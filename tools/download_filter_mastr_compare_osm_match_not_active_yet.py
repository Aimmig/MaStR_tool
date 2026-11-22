from utils.PreConfiguredParser import createDownloadFilterParser
from dotenv import load_dotenv
from download_filter_mastr_compare_osm import compute_matches


if __name__ == "__main__":
    env_file = "env_conf/.compare_match_not_operational_yet"
    load_dotenv(env_file)
    parser = createDownloadFilterParser()
    parser.add_argument('source', nargs='?', const=1, type=str, default="wind")
    arguments = parser.parse_args()
    compute_matches(arguments,
                    distance=25,
                    keep_only_power="generator")
