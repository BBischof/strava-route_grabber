class segment(object):
  def __init__(self, route_id, segment_id, name, segment_index, distance, elev_difference, start_distance, end_distance, ratio, newly_created_segment, avg_grade):
    self.route_id = route_id
    self.segment_id = segment_id
    self.name = name
    self.segment_index = segment_index
    self.distance = distance
    self.elev_difference = elev_difference
    self.start_distance = start_distance
    self.end_distance = end_distance
    self.ratio = ratio
    self.newly_created_segment = newly_created_segment
    self.avg_grade = avg_grade


