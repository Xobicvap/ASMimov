
class EmulatedSystem:

  def __init__(self, systems):
    if len(systems) < 1:
      raise Exception("At least a CPU is required for emulation")
    self.systems = []
    for s in systems:
      self.systems.append(s)

  def step(self):
    # wait for timing signal in later versions
    for system_emulate in self.systems:
      system_emulate.step()

  def get_cpu_state(self):
    return self.systems[0].cpu

  def start(self, override_reset=None):
    self.get_cpu_state().reset(override_reset)

