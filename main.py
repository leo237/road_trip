from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px

STATE_TO_FIPS_ID = {
	'WA' : 53,
	'MT' : 30,
	'ND' : 38,
	'SD' : 46,
	'MN' : 27,
	'WI' : 55,
	'IL' : 17,
	'IN' : 18,
	'OH' : 39
}

FIPS_ID_TO_STATE = {str(val) : key for (key, val) in STATE_TO_FIPS_ID.items()}



def counties_info_by_state(counties_raw_info):
	_PROPERTIES = 'properties'
	_STATE = 'STATE'

	counties_info = {}

	relevant_fips_state_code = [str(val) for _,val in STATE_TO_FIPS_ID.items()]

	unique = set()

	for info in counties_raw_info["features"]:
		state_id = info[_PROPERTIES][_STATE]
		if state_id in relevant_fips_state_code:
			if FIPS_ID_TO_STATE[state_id] not in counties_info:
				counties_info[FIPS_ID_TO_STATE[state_id]] = []
			counties_info[FIPS_ID_TO_STATE[state_id]].append(info)

	return counties_info

def get_raw_counties_info():
	with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
		counties_raw_info = json.load(response)

	return counties_raw_info




if __name__ == '__main__':
	raw_counties_info = get_raw_counties_info()
	counties_by_state = counties_info_by_state(raw_counties_info)

	df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

	
	fig = px.choropleth(df, geojson=raw_counties_info, locations='fips', color='unemp',
	                           color_continuous_scale="Viridis",
	                           range_color=(0, 12),
	                           scope="usa",
	                           labels={'unemp':'unemployment rate'}
	                          )
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
	fig.show()


