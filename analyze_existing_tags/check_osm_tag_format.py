from utils.PreConfiguredParser import createOSMFormatParser
from utils.PlantsFromOSM import getWindPlantsInArea
from utils.CheckOsmTagFormats import *
from utils.Helper import plot
from utils.Constants import POWER, ROTOR, HUB, START, END
from utils.Constants import REF_MASTR, REF_EEG
import pandas as pd


if __name__ == "__main__":
    parser = createOSMFormatParser()
    arguments = parser.parse_args()
    output = arguments.output
    area = arguments.area
    check_col = arguments.tag
    osm_units = getWindPlantsInArea(area, sanitize=True, invalidate_cache=True)
    filtered = None
    cols = None
    if check_col in [POWER]:
        filtered, cols = check_power_value(osm_units, check_col)
    if check_col in [HUB, ROTOR]:
        filtered, cols = check_meter_values(osm_units, check_col)
    if check_col in [START, END]:
        filtered, cols = check_date(osm_units, check_col)
    if check_col in ["name", "description", "note", "ref", REF_MASTR, REF_EEG]:
        filtered, cols = check_name(osm_units, check_col)
    csv = filtered[cols].to_csv(
                output,
                index=False,
                )
    if csv:
        print(csv)
    plot(check_col, cols, filtered)
