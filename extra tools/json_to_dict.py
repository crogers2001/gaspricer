import json
from datetime import datetime

# Define the base date
base_date = datetime.strptime("2023-01-01", "%Y-%m-%d")

# Function to calculate seconds since the base date
def seconds_since_base(date_string):
    try:
        input_date = datetime.strptime(date_string, "%Y-%m-%d")
        time_difference = input_date - base_date
        return int(time_difference.total_seconds())
    except ValueError:
        print(f"Error")
        return None
    
file_path = "wholesale_prices.json"

with open(file_path, "r") as file:
    data = json.load(file)

price_dict = {}
for record in data["response"]["data"]:
    period = record["period"]
    time = seconds_since_base(period)
    value = float(record["value"])
    price_dict[time] = value

# Convert the dictionary to a string
price_dict_string = str(price_dict)

# Save the string to a .txt file
output_file = "parsed_prices.txt"
with open(output_file, "w") as file:
    file.write(price_dict_string)

print(f"Parsed data saved to {output_file}")