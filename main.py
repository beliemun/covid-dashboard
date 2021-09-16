import pandas as pd

daily_df = pd.read_csv("data/daily_reports.csv")
totals_df = daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={"index":"condition"})

countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = countries_df.groupby("Country_Region").sum().reset_index()

conditions = ["confirmed", "deaths", "recovered"]
def make_global_df(condition):
    df = pd.read_csv(f"data/time_{condition}.csv")
    df = df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1).sum().reset_index(name=f"{condition}")
    df = df.rename(columns={"index":"date"})
    return df
final_df = None
for condition in conditions:
    df = make_global_df(condition)
    if final_df is None:
        final_df = df
    else:
        final_df = final_df.merge(df)