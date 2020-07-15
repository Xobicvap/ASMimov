from random import randrange
from architecture.math.hexnum import ByteValue

RANDOMIZE = 1
ZERO_OUT = 0

class MemoryBank:

  def __init__(self, power_on_behavior=0):
    self.memory_map = {}
    self.max_size = 0xffff
    self.power_on_behavior = power_on_behavior

    for i in range(0, self.max_size + 1):
      if self.power_on_behavior == RANDOMIZE:
        self.memory_map[i] = ByteValue(randrange(0, 256))
      elif self.power_on_behavior == ZERO_OUT:
        self.memory_map[i] = ByteValue(0)
      else:
        raise Exception("Unknown power-on behavior specified...")

  def replace_map(self, replacement):
    self.memory_map = replacement

  def read(self, address):
    return self.memory_map[address]

  def write(self, address, value):
    self.memory_map[address] = value

  def __str__(self):
    s = ""
    for k, v in self.memory_map.items():
      if v.value != 0:
        s = s + hex(k) + ": " + hex(v.value) + "\n"
    return s
