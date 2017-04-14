class route(object):
  def __init__(self, route_id, name, length, elevation_gain, route_type, sub_type, popularity, starting_location, end_location):
    self.route_id = route_id
    self.name = name
    self.length = length
    self.elevation_gain = elevation_gain
    self.route_type = route_type
    self.sub_type = sub_type
    self.popularity = popularity
    self.start_latitude = starting_location.latitude
    self.start_longitude = starting_location.longitude
    self.end_latitude = end_location.latitude
    self.end_longitude = end_location.longitude

  def write_row(self):
    return map(str, [
          self.route_id,
          self.name,
          self.length,
          self.elevation_gain,
          self.route_type,
          self.sub_type,
          self.popularity,
          self.start_latitude,
          self.start_longitude,
          self.end_latitude,
          self.end_longitude
        ])
