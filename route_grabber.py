from __future__ import print_function
from flask import Flask
import json, sys
from parsingLibrary import get_route_data as grd
from parsingLibrary import parsing_functions as pf
from parsingLibrary.data_queue import data_queue
app = Flask(__name__)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_routes/<lower_bound>&<upper_bound>")
def process_strava_routes_within_bounds(lower_bound, upper_bound):
    routes_data = [grd.convert_html_tree_to_data_dictionaries(route_number, grd.get_html_tree_from_strava_route_number(route_number))
            for route_number in grd.convert_endpoints_to_range(lower_bound, upper_bound)]
    eprint('Completed GET requests!')
    queue = data_queue()
    for rte in routes_data:
      if rte != None:
        queue.append_rte_content_to_queue(pf.extract_rte_content(rte))
    return ",".join(["\n"+x.name for x in queue.metadata])+"\n"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
