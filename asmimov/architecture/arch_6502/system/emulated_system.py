
class EmulatedSystem:

  def __init__(self, *systems):
    if len(systems) < 1:
      raise Exception("At least a CPU is required for emulation")
    self.systems = systems

