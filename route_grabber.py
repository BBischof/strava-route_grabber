from flask import Flask
import requests
from lxml import html
from lxml.cssselect import CSSSelector
import json
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

def parse_text_into_data_dictionaries(page_text):
    text_athlete, text_pageview = page_text.split("Strava")[2], page_text.split("Strava")[3]
    text_pageview_route_data, text_pageview_route_segments = text_pageview.split('.route')[1], text_pageview.split('.route')[2]
    return {'athlete data': parse_athlete_text_to_dictionary(text_athlete),
        'route data': parse_route_data_text_to_dictionary(text_pageview_route_data),
        'segment data': parse_route_segments_text_to_list_of_dictionary(text_pageview_route_segments)[0]}

def convert_html_tree_to_data_dictionaries(tree):
    for x in tree.iter():
        try:
            if x.tag == 'script' and 'routeSegments' in x.text:
                return parse_text_into_data_dictionaries(x.text)
        except:
            pass

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_routes/<lower_bound>&<upper_bound>")
def process_strava_routes_within_bounds(lower_bound, upper_bound):
    routes_data = [convert_html_tree_to_data_dictionaries(get_html_tree_from_strava_route_number(route_number))
            for route_number in convert_endpoints_to_range(lower_bound, upper_bound)]
    return str(routes_data[0].keys()[0])

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
