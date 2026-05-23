def trend(df):

    start = df.iloc[0]

    end = df.iloc[-1]

    if (
        end.temperature
        >
        start.temperature
    ):

        return "Increasing"

    return "Stable"