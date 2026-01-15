import argparse
from utils.Constants import ENERGY_SOURCES, SELECT_COLS


def createParser():
    """
    Create parser for different cmd line options
    Returns: the preconfigured parser
    """
    parser = argparse.ArgumentParser(
        prog="mastr-tool",
        usage='%(prog)s [options]',
        )
    parser.add_argument(
        "source",
        choices=ENERGY_SOURCES,
        help="The energy source for which to download the data from MaStR",
        )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Optional file to write csv data to",
        )
    parser.add_argument(
        "--keepColumns", "-keep",
        nargs='*',
        choices=SELECT_COLS.keys(),
        help="Which columns to keep, if these exist.")
    parser.add_argument(
        "--discardSmall",
        type=int,
        help="Discard small installations")
    parser.add_argument(
        "--formatPower", "-power",
        nargs='?',
        choices=["kW", "MW"],
        help="Unit to use for formatting the power values",
        )
    parser.add_argument(
        "--formatManufacturer", "-m",
        action=argparse.BooleanOptionalAction,
        help="wether to shorten manufacturer names",
        )
    parser.add_argument(
        "--startDate", "-start",
        action='store_true',
        help="Filter for entries with start date",
        )
    parser.add_argument(
        "--endDate", "-end",
        action='store_true',
        help="Filter for entries with end date",
        )
    parser.add_argument(
        "--openingDate", "-opening",
        action='store_true',
        help="Filter for entries with opening date",
        )
    parser.add_argument(
        "--openingDateFuture", "-future",
        action='store_true',
        help="Filter for entries with opening date in future",
        )
    parser.add_argument(
        "--openingDatePast", "-past",
        action='store_true',
        help="Filter for entries with opening date in past",
        )
    parser.add_argument(
        "--currentlyOperational", "-currently",
        action='store_true',
        help="Filter for entries currently operational",
        )
    parser.add_argument(
        "--offshore",
        action='store_true',
        help="Only offshore",
        )
    parser.add_argument(
        "--onshore",
        action='store_true',
        help="Only onshore",
        )
    parser.add_argument(
        "--eeg",
        action='store_true',
        help="Only with EGGxxx",
        )
    parser.add_argument(
        "--kwk",
        action='store_true',
        help="Only with KWKxxx",
        )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Aditional query string \"key='value' and/or key='value' ....\"",
        )
    parser.add_argument(
        "--plot",
        action='store_true',
        help="wether to plot the data",
        )

    parser.set_defaults(formatPower="kW")
    parser.set_defaults(formatManufacturer=True)
    parser.set_defaults(discardSmall=30)
    return parser
