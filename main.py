import os
from MaStR_WKA import MaStR_WKA as MaStR_WKA

if __name__ == '__main__':
    os.environ['USE_RECOMMENDED_NUMBER_OF_PROCESSES'] = 'True'
    wka = MaStR_WKA()
    wka.preFilter()
    wka.filter_region(state="Rheinland-Pfalz")
    df = wka.get_plants_with_opening_date()
    print(df[wka.print_cols])
    #pv = MaStR_PV()#.get_plants_with_opening_date()
    #print(pv)
