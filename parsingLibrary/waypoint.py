class waypoint(object):
  def __init__(self, route_id, waypoint_index, latitude, longitude):
    self.route_id = route_id
    self.waypoint_index = waypoint_index
    self.latitude = latitude
    self.longitude = longitude

  def write_row(self):
    return map(str, [
      self.route_id,
      self.waypoint_index,
      self.latitude,
      self.longitude
    ])

