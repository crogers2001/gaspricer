import requests
import json

registered_EIA_API_key = 'hidden'
api_url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={registered_EIA_API_key}&frequency=daily&data[0]=value&facets[series][]=EER_EPMRU_PF4_RGC_DPG&start=2022-12-31&end=2023-12-31&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"

headers = {
    "X-Params": json.dumps({
        "frequency": "daily",
        "data": ["value"],
        "facets": {
            "series": ["EER_EPMRU_PF4_RGC_DPG"]
        },
        "start": "2022-12-31",
        "end": "2023-12-31",
        "sort": [
            {
                "column": "period",
                "direction": "asc"
            }
        ],
        "offset": 0,
        "length": 5000
    })
}

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    print("Request successful")
    data = response.json()
    output_file = "wholesale_prices.json"
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response:", response.text)
