import reverse_geocoder as rg

class data_queue(object):
  def __init__(self):
    self.metadata = []
    self.athlete = []
    self.segments = []
    self.waypoints = []

  def append_rte_content_to_queue(self, rte_content):
    self.metadata.append(rte_content[0])
    self.athlete.append(rte_content[1])
    self.segments += rte_content[2]
    self.waypoints += rte_content[3]

  def add_geo_assets(self):
    map(lambda way, geoass: way.add_geo_asset(geoass), self.waypoints, rg.search([(waypoint.latitude, waypoint.longitude) for waypoint in self.waypoints]))
    route_start_geoassets = rg.search([(route.start_latitude, route.start_longitude) for route in self.metadata])
    route_end_geoassets = rg.search([(route.end_latitude, route.end_longitude) for route in self.metadata])
    map(lambda rte, start_geoass, end_geoass: rte.add_geo_asset(start_geoass, end_geoass), self.metadata, route_start_geoassets, route_end_geoassets)
