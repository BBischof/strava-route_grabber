from flask import Flask
import requests
from lxml import html
from lxml.cssselect import CSSSelector
import json
from parsingLibrary.route import route
from parsingLibrary.segment import segment
from parsingLibrary.waypoint import waypoint
from parsingLibrary.athlete import athlete
app = Flask(__name__)

def get_route_data_from_strava_by_number(route_number):
  return requests.get("https://www.strava.com/routes/"+str(route_number))

def convert_endpoints_to_range(lower_bound, upper_bound):
  try:
    return range(int(lower_bound), int(upper_bound))
  except:
    raise ValueError("Incorrect Route Number Values")

def get_html_tree_from_strava_route_number(route_number):
    response = get_route_data_from_strava_by_number(route_number)
    return html.fromstring(response.content)

def parse_athlete_text_to_dictionary(athlete_text):
    return json.loads(athlete_text.strip('.Models.Athlete(').strip(')\n var pageView = new'))

def parse_route_data_text_to_dictionary(route_data_text):
    return json.loads(route_data_text.strip('Data(').strip(')\n      '))

def parse_route_segments_text_to_list_of_dictionary(route_data_text):
    return json.loads(route_data_text.strip('Segments(').strip(')\n      '))

def parse_text_into_data_dictionaries(route_number, page_text):
    text_athlete, text_pageview = page_text.split("Strava")[2], page_text.split("Strava")[3]
    text_pageview_route_data, text_pageview_route_segments = text_pageview.split('.route')[1], text_pageview.split('.route')[2]
    return {
        'route_number': route_number,
        'athlete_data': parse_athlete_text_to_dictionary(text_athlete),
        'route_data': parse_route_data_text_to_dictionary(text_pageview_route_data),
        'segment_data': [x for x in parse_route_segments_text_to_list_of_dictionary(text_pageview_route_segments)]
        }

def convert_html_tree_to_data_dictionaries(route_number, tree):
    for x in tree.iter():
        try:
            if x.tag == 'script' and 'routeSegments' in x.text:
                return parse_text_into_data_dictionaries(route_number, x.text)
        except:
            pass

def extract_waypoint_content(route_number, route_dictionary):
  waypoints_list = [
    waypoint(
      route_number,
      index,
      way['waypoint']['point']['lat'],
      way['waypoint']['point']['lng']
    ) for index, way in enumerate(route_dictionary['route']['elements'])
  ]
  return waypoints_list

def extract_route_metadata(route_number, route_dictionary, starting_location, end_location):
  new_route = route(
    route_number,
    route_dictionary['metadata']['name'].replace(",", "").encode('utf-8'),
    route_dictionary['metadata']['length'], # length in meters
    route_dictionary['metadata']['elevation_gain'], # elevation gain in meters
    route_dictionary['metadata']['route_type'],
    route_dictionary['metadata']['sub_type'],
    route_dictionary['route']['preferences']['popularity'],
    starting_location,
    end_location
  )
  return new_route

def extract_route_content(route_number, route_dictionary):
  waypoints_list = extract_waypoint_content(route_number, route_dictionary)
  new_route = extract_route_metadata(route_number, route_dictionary, waypoints_list[0], waypoints_list[-1])
  return waypoints_list, new_route

def extract_segment_content(route_number, segment_dictionary_list):
  segment_list = [
    segment(
      route_number,
      seg['id'],
      (seg['name'] or "").encode('utf-8').replace(",", ""),
      index,
      seg['distance'],
      seg['elev_difference'],
      seg['start_distance'],
      seg['end_distance'],
      seg['ratio'],
      seg['newly_created_segment'],
      seg['avg_grade']
      ) for index, seg in enumerate(segment_dictionary_list)
    ]
  return segment_list

def correct_city_country_delimiting(city, state):
  '''Handle cases where people poorly enter their city/state'''
  if ("," in city):
    if ("" == state):
      split_city = city.rsplit(",", 1)
      city = split_city[0]
      state = split_city[1]
    city = city.replace(",", "")
  if ("," in state):
    if ("" == city):
      split_city = state.split(",", 1)
      city = split_city[0]
      state = split_city[1]
    state = state.replace(",", "")
  return city, state

def extract_athlete_content(route_number, route_dictionary):
  city, state = correct_city_country_delimiting(route_dictionary['geo']['city'], route_dictionary['geo']['state'])
  new_athlete = athlete(
      route_number,
      route_dictionary['id'],
      route_dictionary['display_name'].replace(",", "").encode('utf-8'),
      city,
      state,
      route_dictionary['geo']['country'],
      route_dictionary['geo']['lat_lng'][0],
      route_dictionary['geo']['lat_lng'][1],
      route_dictionary['member_type']
    )
  return new_athlete


@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_routes/<lower_bound>&<upper_bound>")
def process_strava_routes_within_bounds(lower_bound, upper_bound):
    routes_data = [convert_html_tree_to_data_dictionaries(route_number, get_html_tree_from_strava_route_number(route_number))
            for route_number in convert_endpoints_to_range(lower_bound, upper_bound)]
    for x in routes_data:
      if x != None:
        waypoints, metadata = extract_route_content(x['route_number'], x['route_data'])
        segments = extract_segment_content(x['route_number'], x['segment_data'])
        athletes = extract_athlete_content(x['route_number'], x['athlete_data'])
    return athletes.name
    # return ",".join([x[1]['route_data'] for x in routes_data])

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
