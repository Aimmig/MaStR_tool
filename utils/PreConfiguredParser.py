import argparse
from pyrosm.data import sources
from utils.Constants import ENERGY_SOURCES, SELECT_COLS, COMMON_COLS
from utils.Constants import ROTOR, HUB, POWER
from utils.Constants import REF_EEG, REF_MASTR
from utils.Constants import START, END


def createSimpleMastrQueryParser():
    """
    Custom parser for querying details based on a list
    of some MaStR ref numbers
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options]',
        )
    parser.add_argument(
        "source",
        choices=ENERGY_SOURCES,
        help="The energy source to download and search from MaStR",
        )
    parser.add_argument(
        "--keepColumns", "-keep",
        nargs='*',
        choices=list(SELECT_COLS.keys()) + list(COMMON_COLS.keys()),
        help="Which columns to keep, if these exist.",
        )
    parser.add_argument(
        "ref",
        nargs='+',
        type=str,
        help="The MaStR reference to search, e.g. SEExxx, EEGxxx etc.",
    )
    return parser


def createOSMFormatParser():
    """
    Custom parser for reading the osm pbf file
    and check tags for potentially malformed or
    suspicious things
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options]',
        )
    parser.add_argument(
        "area",
        type=str,
        choices=["germany"] + sources.subregions.germany.available,
        help="area to investigate",
        )
    parser.add_argument(
        "tag",
        type=str,
        choices=[
            ROTOR, HUB,
            POWER,
            "name", "description", "note", "fixme",
            REF_MASTR, REF_EEG, "ref",
            START, END
            ],
        help="osm tag to check formatting",
        )
    return parser


def createParser():
    """
    Custom parser for the main program.
    Different cmd line options
    Returns: the preconfigured parser
    """
    parser = argparse.ArgumentParser(
        prog="mastr-tool",
        usage='%(prog)s [options]',
        )
    parser.add_argument(
        "source",
        choices=ENERGY_SOURCES,
        help="energy source for which to download the data from MaStR",
        )
    parser.add_argument(
        "--keepColumns", "-keep",
        nargs='*',
        choices=SELECT_COLS.keys(),
        help="columns to keep, if these exist.")
    parser.add_argument(
        "--discardSmall",
        type=int,
        help="discard small installations")
    parser.add_argument(
        "--formatPower", "-power",
        nargs='?',
        choices=["kW", "MW"],
        help="Unit to use for formatting the power values",
        )
    parser.add_argument(
        "--formatManufacturer", "-m",
        action=argparse.BooleanOptionalAction,
        help="Whether to shorten manufacturer names",
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
        help="Additional query string \"key='value' and/or key='value' ....\"",
        )
    parser.add_argument(
        "--plot",
        type=str,
        nargs='?',
        help="Whether to plot data and which column to use as colour",
        )
    parser.add_argument(
        "--testagainstOSM",
        type=str,
        nargs='?',
        choices=["germany"] + sources.subregions.germany.available,
        help="Select area to test",
        )

    parser.set_defaults(formatPower="kW")
    parser.set_defaults(formatManufacturer=True)
    parser.set_defaults(discardSmall=30)
    return parser
