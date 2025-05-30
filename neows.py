import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta


app = Flask(__name__)

API_KEY = '' #ur key here

def get_neo_data(start_date, end_date):
    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}'
  
    response = requests.get(url)
    data = response.json()
            
    return data
  

@app.route('/')
def index():
    # for displaying today and tomorrows neows for real time data
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    
    data = get_neo_data(today, tomorrow)
    

    #list data 
    neos = []
    for date in data['near_earth_objects']:
        for neo in data['near_earth_objects'][date]:
            neos.append({
                'name': neo['name'].replace('(', '').replace(')', ''), #names had ()
                'hazardous': neo['is_potentially_hazardous_asteroid'],
                'approach_date': neo['close_approach_data'][0]['close_approach_date'],
                'miss_distance': neo['close_approach_data'][0]['miss_distance']['kilometers'],
                'velocity': neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
            })
    
    return render_template('index.html', neos=neos)

@app.route('/custom_date', methods=['GET', 'POST'])
def custom_date():
    if request.method == 'POST': #form submitted
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        data = get_neo_data(start_date, end_date)
        
     
        neos = []
        for date in data['near_earth_objects']:
            for neo in data['near_earth_objects'][date]:
                neos.append({
                    'name': neo['name'].replace('(', '').replace(')', ''), 
                    'hazardous': neo['is_potentially_hazardous_asteroid'],
                    'approach_date': neo['close_approach_data'][0]['close_approach_date'],
                    'miss_distance': neo['close_approach_data'][0]['miss_distance']['kilometers'],
                    'velocity': neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
                })
        
        return render_template('custom_date.html', neos=neos, start_date=start_date, end_date=end_date)
    
    return render_template('custom_date.html')

if __name__ == '__main__':
    app.run(debug=True) 