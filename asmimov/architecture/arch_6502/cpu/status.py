from math import hexnum

class StatusRegister(hexnum.ByteValue):

  def __init__(self, v):
    super.__init__(v)
    self.names = ["N", "V", "B5", "B4", "D", "I", "Z", "C"]
    for n in self.names:
      setattr(self, n, 0)
    self.set_flags(v)

  def set_flags(self, v, bit_name=None):
    if bit_name is None:
      self.N = v & 0x80
      self.V = v & 0x40
      self.D = v & 0x08
      self.I = v & 0x04
      self.Z = v & 0x02
      self.C = v & 0x01
    else:
      if v != 1 and v != 0:
        raise Exception("Value must be bit when named status flag given")
      if bit_name not in self.names:
        raise Exception("Invalid flag name " + bit_name + " requested for set")
      setattr(self, bit_name, v)

  def get_flag(self, bit_name):
    return getattr(self, bit_name)

  def modify(self, bit_name, value=None):
    if value is None:
      return self.get_flag(bit_name)
    else:
      self.set_flags(value, bit_name)

