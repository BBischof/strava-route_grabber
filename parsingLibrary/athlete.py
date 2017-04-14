class athlete(object):
  def __init__(self, route_id, athlete_id, name, city, state, country, lat, lng, member_type):
    self.route_id = route_id
    self.athlete_id = athlete_id
    self.name = name
    self.city = city
    self.state = state
    self.country = country
    self.lat = lat
    self.lng = lng
    self.member_type = member_type

  def write_row(self):
    return map(str, [
      self.route_id,
        self.athlete_id,
        self.name,
        self.city,
        self.state,
        self.country,
        self.lat,
        self.lng,
        self.member_type
    ])
