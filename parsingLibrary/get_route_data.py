import requests
from lxml import html
from lxml.cssselect import CSSSelector
import json

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
