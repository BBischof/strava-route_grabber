from route import route
from segment import segment
from waypoint import waypoint
from athlete import athlete
from data_queue import data_queue

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
