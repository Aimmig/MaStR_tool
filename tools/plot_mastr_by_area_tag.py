from utils.Mastrdata import get_filtered_mastr_from_args
from utils.Helper import plot
from utils.PreConfiguredParser import createParser
from dotenv import load_dotenv


if __name__ == "__main__":
    # This should be seperated into another file
    enf_file = "env_conf/.env"
    load_dotenv(enf_file)
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
