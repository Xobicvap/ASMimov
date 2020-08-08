

class Aggregator:

  def __init__(self, aggregator_type, use_aggregator):
    self.aggregator_type = aggregator_type
    self.active = use_aggregator
    self.change_map = {}

  def aggregate(self, cycle, **changes):
    if not self.active:
      return None
    if cycle in self.change_map:
      self.change_map[cycle].update(changes)
    else:
      self.change_map[cycle] = changes
