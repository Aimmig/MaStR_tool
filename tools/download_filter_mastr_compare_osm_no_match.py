from utils.PreConfiguredParser import createDownloadFilterParser
from dotenv import load_dotenv
from download_filter_mastr_compare_osm import compute_matches

if __name__ == "__main__":
    env_file = "env_conf/.compare_no_match_env"
    load_dotenv(env_file)
    parser = createDownloadFilterParser()
    parser.add_argument('source', nargs='?', const=1, type=str, default="wind")
    arguments = parser.parse_args()
    compute_matches(arguments,
                    distance=50,
                    drop_or_keep="drop")
