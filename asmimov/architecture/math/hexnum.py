class ByteValue:
  def __init__(self, v):
    self.max_value = 255
    self.value = v
    self.carry_happened = False
    self.bcd = False

  def bit_set(self, bit_pos):
    return self.value & 2**bit_pos != 0

  def bit_at(self, bit_pos):
    return 1 if (self.value & 2**bit_pos) >> bit_pos != 0 else 0

  def negative(self):
    return 1 if self.value > 127 else 0

  def zero(self):
    return 1 if self.value == 0 else 0

  def carry(self):
    return 1 if self.carry_happened else 0

  # for these next methods we should upgrade to python >= 3.7;
  # this will allow type hinting (at much less performance degradation)
  # and allow us to use from __future__ import annotations

  def __add__(self, other):
    # will this be understood in WordValue?
    if other is ByteValue:
      temp = self.value + other.value
    else:
      temp = self.value + other

    if temp > self.max_value:
      self.carry_happened = True
      # handle overflow; temp = 256 - x
      # i.e 0x80 + 0x81 = 0x101 -> 0x101 - 0x100 = 0x01
      temp = temp - self.max_value
    else:
      self.carry_happened = False
    self.value = ByteValue(temp)

  def __sub__(self, other):
    if other is ByteValue:
      temp = self.value - other.value
    else:
      temp = self.value - other
    if temp < 0:
      # what about carry?
      # i.e. 0x90 - 0x92 = -0x02 + 0x100 = 0xfe
      temp = temp + self.max_value
    self.value = ByteValue(temp)

  def __and__(self, other):
    if other is ByteValue:
      self.value = self.value & other.value
    else:
      self.value = self.value & other

  def __or__(self, other):
    if other is ByteValue:
      self.value = self.value | other.value
    else:
      self.value = self.value | other

  def __xor__(self, other):
    if other is ByteValue:
      self.value = self.value ^ other.value
    else:
      self.value = self.value ^ other

  # lshift and rshift expect an integer as 'other'

  def __lshift__(self, other):
    if other != 1:
      raise Exception("Can only shift by one via magic methods")
    if self.bit_set(7):
      self.carry_happened = True
    else:
      self.carry_happened = False
    self.value = self.value << other

  def __rshift__(self, other):
    if other != 1:
      raise Exception("Can only shift by one via magic methods")
    if self.bit_set(0):
      self.carry_happened = True
    else:
      self.carry_happened = False
    self.value = self.value >> other

class WordValue:

  def __init__(self, v, hi_byte=None):
    self.max_value = 65536
    if v < 256 and hi_byte is not None:
      if hi_byte < 256:
        self.lo_byte = super.__init__(v)
        self.hi_byte = super.__init__(hi_byte)
        self.value = (hi_byte << 8) + v
      else:
        raise Exception("Incorrect init for WordValue; hi_byte must be < 256")
    else:
      if v >= self.max_value:
        raise Exception("WordValue must be < 65536 / 0xffff")
      self.value = v
      if v < 256:
        self.hi_byte = 0
        self.lo_byte = v
      else:
        self.lo_byte = v & 0xff
        self.hi_byte = v & 0xff00

  def get(self):
    return self.value

  def get_lo_byte(self):
    return self.lo_byte

  def get_hi_byte(self):
    return self.hi_byte

  def set_lo_byte(self, lo_byte):
    self.lo_byte = lo_byte
    if self.hi_byte < 256:
      temp_hi_byte = self.hi_byte << 8
    self.value = temp_hi_byte + self.lo_byte

  def set_hi_byte(self, hi_byte):
    temp_hi_byte = hi_byte << 8
    self.value = temp_hi_byte + self.lo_byte

  def __add__(self, other):
    self.value = self.value + other

  def __sub__(self, other):
    self.value = self.value - other
