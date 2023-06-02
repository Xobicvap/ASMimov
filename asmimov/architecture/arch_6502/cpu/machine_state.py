
DEFAULTS = {
  "graphics": False,
  "mixed": False,
  "page": True,
  "hi_res": False,
  "keyboard_data": 0x00
}

class MachineState:
  def __init__(self, defaults=None):
    if defaults is None:
      defaults = DEFAULTS
    self.defaults = defaults

