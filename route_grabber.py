from __future__ import print_function
from flask import Flask
import sys, os
from parsingLibrary import get_route_data as grd
from parsingLibrary import parsing_functions as pf
from parsingLibrary.data_queue import data_queue
from util.databaseConnection import DatabaseConnection as dbConn
app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_routes/<lower_bound>&<upper_bound>")
def process_strava_routes_within_bounds(lower_bound, upper_bound):
    connection = dbConn(DATABASE_URL)
    connection.rds_connect()
    connection.insert_rows_into_table([{"id":  0000, "athlete_id":  0000, "name":  'test', "length_in_meters":  0, "elevation_gain_in_meters": 0, "route_type":  0, "sub_type":  0, "popularity": True , "start_lat":  0.0, "start_lon":  0.0, "starting_point_geo_asset_name":  'start', "starting_point_geo_asset_cc":  'start_cc', "starting_point_geo_asset_admin1":  'start_admin', "starting_point_geo_asset_admin2":  'start_admin2', "end_lat":  0.0, "end_lon":  0.0, "ending_point_geo_asset_name":  'end', "ending_point_geo_asset_cc":  'end_cc', "ending_point_geo_asset_admin1":  'end_admin', "ending_point_geo_asset_admin2":  'end_admin2'}], 'routes')
    routes_data = [grd.convert_html_tree_to_data_dictionaries(route_number, grd.get_html_tree_from_strava_route_number(route_number))
            for route_number in grd.convert_endpoints_to_range(lower_bound, upper_bound)]
    eprint('Completed GET requests!')
    queue = data_queue()
    for rte in routes_data:
      if rte != None:
        queue.append_rte_content_to_queue(pf.extract_rte_content(rte))
    queue.add_route_and_waypoints_geo_assets()
    return "\n".join([",".join(x.write_row()) for x in queue.metadata])+"\n"
    # return "\n".join([(x.write_row()[0]+" "+x.write_row()[1]+" "+x.write_row()[-5]+" "+x.write_row()[-4]) for x in queue.segments])+"\n"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
