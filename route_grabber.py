from flask import Flask
import requests
from lxml import html
from lxml.cssselect import CSSSelector
import json
from parsingLibrary.route import route
from parsingLibrary.segment import segment
from parsingLibrary.waypoint import waypoint
from parsingLibrary.athlete import athlete
from parsingLibrary.data_queue import data_queue
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

def parse_text_into_data_dictionaries(route_number, script_content_text):
    athlete_text, pageview_text = script_content_text.split("Strava")[2], script_content_text.split("Strava")[3]
    pageview_text_route_data, pageview_text_route_segments = pageview_text.split('.route')[1], pageview_text.split('.route')[2]
    return {
        'route_number': route_number,
        'athlete_data': parse_athlete_text_to_dictionary(athlete_text),
        'route_data': parse_route_data_text_to_dictionary(pageview_text_route_data),
        'segment_data': [x for x in parse_route_segments_text_to_list_of_dictionary(pageview_text_route_segments)]
        }

def convert_html_tree_to_data_dictionaries(route_number, tree):
    for key in tree.iter():
        try:
            if key.tag == 'script' and 'routeSegments' in key.text:
                return parse_text_into_data_dictionaries(route_number, key.text)
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

def extract_rte_content(rte):
  rte_waypoints, rte_metadata = extract_route_content(rte['route_number'], rte['route_data'])
  rte_segments = extract_segment_content(rte['route_number'], rte['segment_data'])
  rte_athlete = extract_athlete_content(rte['route_number'], rte['athlete_data'])
  return (rte_metadata, rte_athlete, rte_segments, rte_waypoints)

def append_rte_content_to_queue(queue, rte_content):
  queue.metadata.append(rte_content[0])
  queue.athlete.append(rte_content[1])
  queue.segments.append(rte_content[2])
  queue.waypoints.append(rte_content[3])


@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_routes/<lower_bound>&<upper_bound>")
def process_strava_routes_within_bounds(lower_bound, upper_bound):
    routes_data = [convert_html_tree_to_data_dictionaries(route_number, get_html_tree_from_strava_route_number(route_number))
            for route_number in convert_endpoints_to_range(lower_bound, upper_bound)]
    queue = data_queue()
    for rte in routes_data:
      if rte != None:
        append_rte_content_to_queue(queue, extract_rte_content(rte))
    return ",".join(["\n"+x.name for x in queue.metadata])+"\n"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
