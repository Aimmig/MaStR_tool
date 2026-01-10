def apply_and_print(function, df, cols=None):
    df = function(df)
    print(function.__name__)
    if cols:
        print(df[cols])
    else:
        print(df)
    print("----------------------")
