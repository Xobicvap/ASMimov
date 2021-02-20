from architecture.math.hexnum import ByteValue

class StatusRegister(ByteValue):

  def __init__(self, v):
    super().__init__(v)
    self.names = ["N", "V", "B5", "B4", "D", "I", "Z", "C"]
    self.N = self.bit_at(7)
    self.V = self.bit_at(6)
    self.D = self.bit_at(3)
    self.I = self.bit_at(2)
    self.Z = self.bit_at(1)
    self.C = self.bit_at(0)

  def set_flags(self, v, flag_name=None):
    if flag_name is None:
      v = ByteValue(v)
      self.N = v.bit_at(7)
      self.V = v.bit_at(6)
      self.D = v.bit_at(3)
      self.I = v.bit_at(2)
      self.Z = v.bit_at(1)
      self.C = v.bit_at(0)
    else:
      if v != 1 and v != 0:
        raise Exception("Value must be bit when named status flag given")
      if flag_name not in self.names:
        raise Exception("Invalid flag name " + flag_name + " requested for set")
      setattr(self, flag_name, v)

  def get_flag(self, flag_name):
    return getattr(self, flag_name.upper())

  def modify(self, flag_name, value=None):
    if value is None:
      return self.get_flag(flag_name)
    else:
      self.set_flags(value, flag_name)

  def __repr__(self):
    return super().__repr__()

  def __str__(self):
    return super().__str__()

