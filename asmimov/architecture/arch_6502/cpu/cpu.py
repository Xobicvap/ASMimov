from .address_bus import AddressBus
from architecture.math.hexnum import ByteValue, WordValue

class CPU:

  def __init__(self, registers, memory):
    self.registers = registers
    self.address_bus = AddressBus(memory)
    self.data_register = ByteValue(0)
    self.instruction_register = ByteValue(0)
    self.vectors = {
      "NMI": 0xFFFA,
      "IRQ": 0xFFFC,
      "RESET": 0xFFFE
    }

  def vector(self, name, next_byte=False):
    if name not in self.vectors:
      raise Exception("Unknown vector " + name + " requested")
    vec_addr = self.vectors[name]
    return vec_addr if not next_byte else vec_addr + 1

  def register(self, name, value=None):
    if value is None:
      return self.registers.read(name)
    else:
      self.registers.write(name, value)

  def sp(self, value=None):
    return self.register("SP", value)

  def p(self, value=None):
    return self.register("P", value)

  def a(self, value=None):
    return self.register("A", value)

  def x(self, value=None):
    return self.register("X", value)

  def y(self, value=None):
    return self.register("Y", value)

  def pc(self, value=None):
    return self.register("PC", value)

  def status_register(self, name, value=None):
    p = self.p()
    return p.modify(name, value)

  def n(self, value=None):
    return self.status_register("N", value)

  def v(self, value=None):
    return self.status_register("V", value)

  def d(self, value=None):
    return self.status_register("D", value)

  def i(self, value=None):
    return self.status_register("I", value)

  def z(self, value=None):
    return self.status_register("Z", value)

  def c(self, value=None):
    return self.status_register("C", value)

  def IR(self, value=None):
    if value is None:
      return self.instruction_register
    self.instruction_register.set_value(value)

  def DR(self, value=None):
    if value is None:
      return self.data_register
    self.data_register.set_value(value)


