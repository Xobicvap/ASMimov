
ALLOWED_KEYWORDS = ["name", "readfxn", "writefxn", "address"]


def kw_allowed(kw):
  if kw in ALLOWED_KEYWORDS:
    return True
  raise TypeError(kw + " not a known IORegister parameter")


class IORegister:
  def __init__(self, *args):
    for reg_def in args:
      keyword_status = [kw_allowed(k) for k in reg_def]
      if len(keyword_status) != len(ALLOWED_KEYWORDS):
        raise AttributeError(str(ALLOWED_KEYWORDS) + " are required")
      for k, v in reg_def.items():
        setattr(self, k, v)

  def read(self, machine_state):
    return self.readfxn(machine_state)

  def write(self, machine_state, value):
    return self.writefxn(machine_state)

  def at(self, address):
    return self.address == address


class IORegisters:
  def __init__(self, reg_defs):
    self.registers = []
    for reg_def in reg_defs:
      self.registers.append(IORegister(**reg_def))

  def get(self, address):
    for reg in self.registers:
      if reg.at(address):
        return reg
    return None

  def read(self, address, machine_state):
    register = self.get(address)
    if register is not None:
      return register.read(machine_state)

  def write(self, address, machine_state, value):
    register = self.get(address)
    if register is not None:
      return register.write(machine_state, value)








