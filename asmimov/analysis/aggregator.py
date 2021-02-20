

class Aggregator:

  def __init__(self, aggregator_type, use_aggregator):
    self.aggregator_type = aggregator_type
    self.active = use_aggregator
    self.change_map = {}

  def stringify(self):
    s = ""
    for cycle, changemap in self.change_map.items():
      s = s + str(cycle) + ": {"
      for k, v in changemap.items():
        if not isinstance(k, str):
          s = s + str(hex(k)) + ": " + str(v) + ", "
        else:
          s = s + k + ": " + str(v) + ", "
      s = s + "}\n"
    return s

  def __str__(self):
    return self.stringify()

  def __repr__(self):
    return self.stringify()

  def aggregate(self, cycle, changes):
    if not self.active:
      return None
    if cycle not in self.change_map:
      self.change_map[cycle] = {}

    for k, v in changes.items():
      self.change_map[cycle][k] = v
