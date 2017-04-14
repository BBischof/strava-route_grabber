class waypoint(object):
  def __init__(self, route_id, waypoint_index, latitude, longitude):
    self.route_id = route_id
    self.waypoint_index = waypoint_index
    self.latitude = latitude
    self.longitude = longitude
    self.geo_asset = {'name': "", 'cc': "", 'admin1': "", 'admin2': ""}

  def add_geo_asset(self, geo_asset):
    self.geo_asset = geo_asset

  def write_row(self):
    return map(str, [
      self.route_id,
      self.waypoint_index,
      self.latitude,
      self.longitude,
      self.geo_asset['name'],
      self.geo_asset['cc'],
      self.geo_asset['admin1'],
      self.geo_asset['admin2']
    ])

