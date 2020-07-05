class ByteValue:
  def __init__(self, v):
    self.max_value = 256
    if v >= self.max_value:
      raise Exception("ByteValue must be < 256")

    self.value = v
    self.carry_happened = False
    self.bcd = False

  # i don't think we need a getter here

  def handle_overflow(self, override_carry=False):
    if self.value >= self.max_value:
      self.carry_happened = True if not override_carry else self.carry_happened
      self.value = self.value - self.max_value
    else:
      self.carry_happened = False if not override_carry else self.carry_happened

  def handle_underflow(self, override_carry=False):
    if self.value < 0:
      self.carry_happened = True if not override_carry else self.carry_happened
      self.value = self.value + self.max_value
    else:
      self.carry_happened = False if not override_carry else self.carry_happened

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

  # for add/sub we need to handle BCD

  def __add__(self, other):
    temp = ByteValue(self.value)
    if isinstance(other, ByteValue):
      temp.value = temp.value + other.value
    else:
      temp.value = temp.value + other

    temp.handle_overflow()
    return temp

  def __sub__(self, other):
    temp = ByteValue(self.value)
    if isinstance(other, ByteValue):
      temp.value = self.value - other.value
    else:
      temp.value = self.value - other

    temp.handle_underflow()
    return temp

  def __and__(self, other):
    temp = ByteValue(self.value)
    if isinstance(other, ByteValue):
      temp.value = temp.value & other.value
    else:
      temp.value = temp.value & other
    return temp

  def __or__(self, other):
    temp = ByteValue(self.value)
    if isinstance(other, ByteValue):
      temp.value = temp.value | other.value
    else:
      temp.value = temp.value | other
    return temp

  def __xor__(self, other):
    temp = ByteValue(self.value)
    if isinstance(other, ByteValue):
      temp.value = temp.value ^ other.value
    else:
      temp.value = temp.value ^ other
    return temp

  # lshift and rshift expect an integer as 'other'

  def __lshift__(self, other):
    if other != 1:
      raise Exception("Can only shift by one via magic methods")
    if self.bit_set(7):
      self.carry_happened = True
    else:
      self.carry_happened = False
    self.value = self.value << other
    self.handle_overflow(True)
    return self

  def __rshift__(self, other):
    if other != 1:
      raise Exception("Can only shift by one via magic methods")
    if self.bit_set(0):
      self.carry_happened = True
    else:
      self.carry_happened = False
    self.value = self.value >> other
    self.handle_underflow(True)
    return self

  def __str__(self):
    if self.value < 0x10:
      return "0" + hex(self.value)[2:].upper()
    return hex(self.value)[2:].upper()

class WordValue:

  def __init__(self, v, hi_byte=None):
    self.max_value = 65536
    if hi_byte is not None:
      self.lo_byte = ByteValue(v)
      self.hi_byte = ByteValue(hi_byte)
      self.value = (hi_byte << 8) + v
    else:
      if v >= self.max_value:
        raise Exception("WordValue must be < 65536 / 0xffff")
      self.value = v
      if v < 256:
        self.hi_byte = ByteValue(0)
        self.lo_byte = ByteValue(v)
      else:
        self.lo_byte = ByteValue(v & 0xff)
        self.hi_byte = ByteValue(v >> 8)

  def get(self):
    return self.value

  def get_lo_byte(self):
    return self.lo_byte

  def get_hi_byte(self):
    return self.hi_byte

  def set_lo_byte(self, lo_byte):
    self.lo_byte = ByteValue(lo_byte)
    temp_hi_byte = self.hi_byte.value
    self.value = (temp_hi_byte << 8) + self.lo_byte.value

  def set_hi_byte(self, hi_byte):
    self.hi_byte = ByteValue(hi_byte)
    temp_hi_byte = hi_byte << 8
    self.value = temp_hi_byte + self.lo_byte.value

  def __add__(self, other):
    if isinstance(other, ByteValue):
      temp = self.value + other.value
    else:
      temp = self.value + other
    if temp > self.max_value:
      temp = temp - self.max_value
    return WordValue(temp)

  def __sub__(self, other):
    if isinstance(other, ByteValue):
      temp = self.value - other.value
    else:
      temp = self.value - other
    if temp < 0:
      temp = temp + self.max_value
    return WordValue(temp)
