from socket import TCP_KEEPINTVL
import requests

import pandas as pd


url = "https://api.stlouisfed.org/fred/series/observations"
headers = {"User-Agent": "MyApp/1.0 (amitjaikumar@g.ucla.edu)"}


series_id = "SP500"

try:
    responses = requests.get(url, headers=headers, timeout=30)
    responses.raise_for_status()
    company = responses.json()
    observations = company.get("observations", [])

    if name:
        print(name)
    else:
        print("entityName not present in response")
except requests.HTTPError as e:
    print("error:", e)
except requests.RequestException as e:
    print("error:", e)
except ValueError as e:
    print("error:", e)

facts = company["facts"]["us-gaap"]
def get_value(year):
    yearly_data = df[df["date"].dt.year == year]

    if yearly_data.empty:
        print("No FRED data found for:", year)
        return None

    latest_observation = yearly_data.iloc[-1]
    return latest_observation["value"]


years = [2020, 2021, 2022, 2023, 2024, 2025]

for year in years:
    value = get_value(year)

    if value is not None:
        print(year, "year-end", series_id, "value:", value)


# Put the lists into a table.
df = pd.DataFrame({
        "Year": years,
       
    })