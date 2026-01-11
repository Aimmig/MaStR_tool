import pandas as pd


def apply_and_print(function, df: pd.DataFrame,
                    cols=None, file_name: str = None):
    df = function(df)
    print(function.__name__)
    if cols:
        df = df[list(cols.keys())]
        df = df.rename(cols, axis='columns')
        print(df)
        df.to_csv(file_name)
    else:
        print(df)
    print("----------------------")
