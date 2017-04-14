class data_queue(object):
  def __init__(self):
    self.metadata = []
    self.athlete = []
    self.segments = []
    self.waypoints = []

  def append_rte_content_to_queue(self, rte_content):
    self.metadata.append(rte_content[0])
    self.athlete.append(rte_content[1])
    self.segments.append(rte_content[2])
    self.waypoints.append(rte_content[3])
