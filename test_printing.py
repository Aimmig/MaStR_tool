def apply_and_print(function, df):
    df = function(df)
    print(function.__name__)
    print(df)
    print("----------------------")
