import requests

API_KEY = '' 
start_date = '2025-05-30'
end_date = '2025-05-30'

url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}'

response = requests.get(url)
data = response.json()

# Example: print names of NEOs
for date in data['near_earth_objects']:
    for neo in data['near_earth_objects'][date]:
        print(f"Name: {neo['name']}, Hazardous: {neo['is_potentially_hazardous_asteroid']}")
        print(f"closest approach date: {neo['close_approach_data']}")
