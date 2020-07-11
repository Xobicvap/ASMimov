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
    self.normal_registers = ['A', 'X', 'Y']

  def write(self, name, value):
    upper_name = name.upper()
    if upper_name in self.normal_registers:
      register = value if isinstance(value, ByteValue) \
        else ByteValue(value)
    elif upper_name == 'SP':
      register = value if isinstance(value, StackPointer) \
        else StackPointer(value)
    elif upper_name == 'P':
      register = value if isinstance(value, StatusRegister) \
          else StatusRegister(value)
    elif upper_name == 'PC':
      register = value if isinstance(value, WordValue) \
          else WordValue(value)
    else:
      raise Exception("Unknown register being written to: " + name)
    setattr(self, name.lower(), register)

  def read(self, name):
    if name not in self.register_names:
      raise Exception(name + " not in register names when getting!")
    return getattr(self, name.lower())
