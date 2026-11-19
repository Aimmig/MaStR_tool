from utils.Mastrdata import get_filtered_mastr_from_args
from utils.Helper import plot
from utils.PreConfiguredParser import createParser
from dotenv import load_dotenv


def generic_by_area(env_file):
    load_dotenv(env_file)
    parser = createParser()
    arguments = parser.parse_args()
    mastr_units, cols = get_filtered_mastr_from_args(arguments)
    plot(arguments.plot, cols, mastr_units)
    csv = mastr_units[cols].to_csv(
                None,
                index=False,
                )
    if csv:
        print(csv)


if __name__ == "__main__":
    env_file = "env_conf/.generic_by_area_env"
    generic_by_area(env_file)
