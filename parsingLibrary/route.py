from vincenty import vincenty

class route(object):
  def __init__(self, route_id, name, length, elevation_gain, route_type, sub_type, popularity, starting_location, end_location, athlete_id):
    self.route_id = route_id
    self.name = name
    self.length = length
    self.elevation_gain = elevation_gain
    self.route_type = route_type
    self.sub_type = sub_type
    self.popularity = popularity
    self.start_latitude = starting_location.latitude
    self.start_longitude = starting_location.longitude
    self.starting_point_geo_asset = {'name': "", 'cc': "", 'admin1': "", 'admin2': ""}
    self.end_latitude = end_location.latitude
    self.end_longitude = end_location.longitude
    self.ending_point_geo_asset = {'name': "", 'cc': "", 'admin1': "", 'admin2': ""}
    self.start_end_separation_in_meters = self.compute_start_end_separation_in_meters(starting_location, end_location)
    self.athlete_id = athlete_id

  def compute_start_end_separation_in_meters(self, starting_location, end_location):
    return vincenty((starting_location.latitude, starting_location.longitude), (end_location.latitude, end_location.longitude))*1000

  def add_geo_asset(self, starting_point_geo_asset, ending_point_geo_asset):
    self.starting_point_geo_asset = starting_point_geo_asset
    self.ending_point_geo_asset = ending_point_geo_asset

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
          self.starting_point_geo_asset['name'],
          self.starting_point_geo_asset['cc'],
          self.starting_point_geo_asset['admin1'],
          self.starting_point_geo_asset['admin2'],
          self.end_latitude,
          self.end_longitude,
          self.ending_point_geo_asset['name'],
          self.ending_point_geo_asset['cc'],
          self.ending_point_geo_asset['admin1'],
          self.ending_point_geo_asset['admin2'],
          self.start_end_separation_in_meters,
          self.athlete_id
        ])
