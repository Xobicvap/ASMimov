from architecture.math.hexnum import ByteValue, WordValue
from .status import StatusRegister
from .stack_pointer import StackPointer

class Registers:

  def __init__(self):
    self.a = ByteValue(0)
    self.x = ByteValue(0)
    self.y = ByteValue(0)
    self.sp = StackPointer(0)
    self.p = StatusRegister(0)
    self.pc = WordValue(0)
    self.register_names = ['A', 'X', 'Y', 'SP', 'P', 'PC']

  def write(self, name, value):
    if name not in self.register_names:
      raise Exception(name + " not in register names for set!")
    register = getattr(self, name.upper())
    register.set_value(value)

  def read(self, name):
    if name not in self.register_names:
      raise Exception(name + " not in register names when getting!")
    return getattr(self, name)
