import requests

import pandas as pd


url = "https://api.stlouisfed.org/fred/series/observations"
api_key = "MyApp/1.0 (amitjaikumar@g.ucla.edu)"


series_id = "SP500"

try:
    responses = requests.get(url,params={"series_id": series_id,"api_key": api_key,"file_type": "json"}, timeout=30)
    responses.raise_for_status()
    fred_data = responses.json()
    observations = fred_data.get("observations", [])

    if observations:
        print(observations)
    else:
        print("observations not present in response")
except requests.HTTPError as e:
    print("error:", e)
except requests.RequestException as e:
    print("error:", e)
except ValueError as e:
    print("error:", e)

years = [2020, 2021, 2022, 2023, 2024, 2025]

# Put the lists into a dataframe.
df = pd.DataFrame(observations)
df["date"] = pd.to_datetime(df["date"])
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna(subset=["value"]).sort_values("date")

def get_value(year):
    yearly_data = df[df["date"].dt.year == year]

    if yearly_data.empty:
        print("No FRED data found for:", year)
        return None

    latest_observation = yearly_data.iloc[-1]
    return latest_observation["value"]

for year in years:
    value = get_value(year)

    if value is not None:
        print(year, "year-end", series_id, "value:", value)