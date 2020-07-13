class ByteValue:
  def __init__(self, v):
    self.max_value = 256
    if v >= self.max_value:
      raise Exception("ByteValue must be < 256")

    self.value = v
    self.carry_happened = False
    self.overflow_happened = False
    self.unsigned = False

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
    if self.unsigned:
      self.unsigned = False
      return 0
    return 1 if self.value > 127 else 0

  def overflow(self, as_bool):
    if as_bool:
      return self.overflow_happened
    return 1 if self.overflow_happened else 0

  def zero(self):
    return 1 if self.value == 0 else 0

  def carry(self, as_bool=False):
    if as_bool:
      return self.carry_happened
    return 1 if self.carry_happened else 0

  def compute_overflow(self, other_byte, temp_negative, temp):
    if other_byte.negative() and temp_negative:
      if not temp.negative():
        temp.overflow_happened = True
    elif not other_byte.negative() and not temp_negative:
      if temp.negative():
        temp.overflow_happened = True
    return temp

  # for these next methods we should upgrade to python >= 3.7;
  # this will allow type hinting (at much less performance degradation)
  # and allow us to use from __future__ import annotations

  # for add/sub we need to handle BCD

  def __add__(self, other):
    temp = ByteValue(self.value)
    temp_negative = temp.negative()

    if isinstance(other, ByteValue):
      temp.value = temp.value + other.value
      other_byte = other
    else:
      temp.value = temp.value + other
      other_byte = ByteValue(other)

    temp = self.compute_overflow(other_byte, temp_negative, temp)
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

class DecimalByteValue(ByteValue):

  def zero(self):
    return 1 if self.value == 0 and not self.carry_happened else 0

  def __add__(self, other):

    temp_negative = self.negative()
    if isinstance(other, DecimalByteValue):
      other_value = other.value
      other_byte = other
    else:
      other_value = other
      other_byte = DecimalByteValue(other)

    temp_value = self.value
    dec_hi_nibble_temp = (temp_value & 0xf0) >> 4
    dec_lo_nibble_temp = temp_value & 0x0f
    dec_hi_nibble_other = (other_value & 0xf0) >> 4
    dec_lo_nibble_other = other_value & 0x0f

    dec_lo_nibble_result = dec_lo_nibble_temp + dec_lo_nibble_other
    dec_hi_nibble_result = dec_hi_nibble_temp + dec_hi_nibble_other
    if dec_lo_nibble_result > 9:
      dec_hi_nibble_result = dec_hi_nibble_result + 1
      dec_lo_nibble_result = dec_lo_nibble_result - 10

    dec_hi_nibble_result = dec_hi_nibble_result * 10
    temp_result = dec_hi_nibble_result + dec_lo_nibble_result
    carry = temp_result > 99
    if carry:
      temp_result = temp_result - 100
      self.carry_happened = True
    xstr = "0x" + str(temp_result)
    x = int(xstr, 16)

    temp = DecimalByteValue(x)
    temp = self.compute_overflow(other_byte, temp_negative, temp)

    return temp

  def __sub__(self, other):

    temp_negative = self.negative()
    if isinstance(other, DecimalByteValue):
      other_value = other.value
      other_byte = other
    else:
      other_value = other
      other_byte = DecimalByteValue(other)

    temp_value = self.value
    dec_hi_nibble_temp = (temp_value & 0xf0) >> 4
    dec_lo_nibble_temp = temp_value & 0x0f
    dec_hi_nibble_other = (other_value & 0xf0) >> 4
    dec_lo_nibble_other = other_value & 0x0f

    if self.value < other.value:
      if dec_lo_nibble_other < dec_lo_nibble_temp:
        dec_lo_nibble_other = dec_lo_nibble_other + 10
        dec_hi_nibble_other = dec_hi_nibble_other - 1
        dec_lo_result = dec_lo_nibble_other - dec_lo_nibble_temp
        dec_hi_result = dec_hi_nibble_other - dec_hi_nibble_temp
      tens = dec_hi_result * 10
      temp_result = tens + dec_lo_result
      temp_result = -temp_result
      temp_result = 100 + temp_result
    else:
      if dec_lo_nibble_temp < dec_lo_nibble_other:
        dec_lo_nibble_temp = dec_lo_nibble_temp + 10
        dec_hi_nibble_temp = dec_hi_nibble_temp - 1

        dec_lo_result = dec_lo_nibble_temp - dec_lo_nibble_other
        dec_hi_result = dec_hi_nibble_temp - dec_hi_nibble_other

        tens = dec_hi_result * 10
        temp_result = tens + dec_lo_result
    carry = temp_result > 99
    if carry:
      temp_result = temp_result - 100
      self.carry_happened = True
    xstr = "0x" + str(temp_result)
    x = int(xstr, 16)

    temp = DecimalByteValue(x)
    temp = self.compute_overflow(other_byte, temp_negative, temp)

    return temp

  def __sub__(self, other):
    temp = ByteValue(self.value)
    if isinstance(other, ByteValue):
      temp.value = self.value - other.value
    else:
      temp.value = self.value - other

    temp.handle_underflow()
    return temp

class WordValue:

  def __init__(self, v, hi_byte=None):
    self.max_value = 65536
    if hi_byte is not None:
      if isinstance(v, ByteValue):
        self.lo_byte = v
      else:
        self.lo_byte = ByteValue(v)
      if isinstance(hi_byte, ByteValue):
        self.hi_byte = hi_byte
      else:
        self.hi_byte = ByteValue(hi_byte)

      self.value = (self.hi_byte.value << 8) + self.lo_byte.value
      self.page_boundary_down = False
      self.page_boundary_up = False
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

  def reset_page_boundaries(self):
    self.page_boundary_up = False
    self.page_boundary_down = False

  def page_boundaries_crossed(self):
    return self.page_boundary_down or self.page_boundary_up

  def fix_page_boundaries(self):
    needed_fix = False
    if self.page_boundary_down:
      self.hi_byte = self.hi_byte - 1
      needed_fix = True
    elif self.page_boundary_up:
      self.hi_byte = self.hi_byte + 1
      needed_fix = True
    return needed_fix

  def set_lo_byte(self, lo_byte):
    self.lo_byte = ByteValue(lo_byte)
    temp_hi_byte = self.hi_byte.value
    self.value = (temp_hi_byte << 8) + self.lo_byte.value

  def set_hi_byte(self, hi_byte):
    self.hi_byte = ByteValue(hi_byte)
    temp_hi_byte = hi_byte << 8
    self.value = temp_hi_byte + self.lo_byte.value

  def __add__(self, other):
    temp_other = other
    if not isinstance(other, ByteValue):
      temp_other = ByteValue(other)

    temp_hi = self.hi_byte
    if temp_other.negative():

      twos_comp = (temp_other.value ^ 0xff) + 1
      temp_lo = self.lo_byte - twos_comp
      if temp_lo.carry(True):
        self.page_boundary_down = True
      else:
        self.page_boundary_down = False
      self.page_boundary_up = False
    else:
      temp_lo = self.lo_byte + temp_other
      if temp_lo.carry(True):
        self.page_boundary_up = True
      self.page_boundary_down = False
    temp = WordValue(temp_lo, temp_hi)
    temp.page_boundary_down = self.page_boundary_down
    temp.page_boundary_up = self.page_boundary_up
    return temp

  def __sub__(self, other):
    if isinstance(other, ByteValue):
      temp = self.value - other.value
    else:
      temp = self.value - other
    if temp < 0:
      temp = temp + self.max_value
    return WordValue(temp)
