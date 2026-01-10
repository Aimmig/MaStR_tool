from energycarrier import MaStR_EEG_Base as base
import pandas as pd
from datetime import date

today = date.today().isoformat()


class MaStR_biomass(base.MaStR_EEG_Base):

    def __init__(self):
        super().__init__("biomass")
