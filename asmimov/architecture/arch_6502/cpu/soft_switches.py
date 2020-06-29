
class SoftSwitches:

  def __init__(self, switches={}):
    self.switches = switches

  def __contains__(self, item):
    return item in self.switches

  def run(self, address):
    pass
