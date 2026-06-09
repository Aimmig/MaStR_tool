from utils.Mastrdata import download
from utils.Constants import MASTR_REFS, SELECT_COLS, COMMON_COLS

if __name__ == "__main__":

    df_full = download("wind")
    ref_list = df_full[[MASTR_REFS['E'], MASTR_REFS['SEE']]]
    ref_list = ref_list.dropna(subset=[MASTR_REFS['E']])
    ref_list.rename(columns=SELECT_COLS | COMMON_COLS, inplace=True)
    csv = ref_list.to_csv(None, index=False)
    if csv:
        print(csv)
