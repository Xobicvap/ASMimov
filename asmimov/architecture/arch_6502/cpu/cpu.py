from .address_bus import AddressBus
from analysis.aggregator import Aggregator
from architecture.math.hexnum import ByteValue, WordValue


class CPU:

  def __init__(self, registers, memory, use_aggregator=False):
    self.registers = registers
    self.address_bus = AddressBus(memory)
    self.data_register = ByteValue(0)
    self.d2 = ByteValue(0)
    self.instruction_register = ByteValue(0)
    self.vectors = {
      "NMI": 0xFFFA,
      "RESET": 0xFFFC,
      "IRQ": 0xFFFE
    }
    self.fix_effective = False
    self.use_aggregator = use_aggregator
    self.change_map = {}

  def write_change(self, name, value):
    if self.use_aggregator:
      self.change_map.update({name: value})

  def vector(self, name, next_byte=False):
    if name not in self.vectors:
      raise Exception("Unknown vector " + name + " requested")
    vec_addr = self.vectors[name]
    return WordValue(vec_addr) if not next_byte else WordValue(vec_addr + 1)

  def irq_vector(self, next_byte=False):
    return self.vector("IRQ", next_byte)

  def reset_vector(self, next_byte=False):
    return self.vector("RESET", next_byte)

  def nmi_vector(self, next_byte=False):
    return self.vector("NMI", next_byte)

  def register(self, name, value=None):
    if value is None:
      return self.registers.read(name)
    else:
      self.registers.write(name, value)
      self.write_change(name, value)

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
    self.instruction_register = value if isinstance(value, ByteValue) else \
      ByteValue(value)

  def DR(self, value=None):
    if value is None:
      return self.data_register
    self.data_register = value if isinstance(value, ByteValue) else \
      ByteValue(value)

  def D2(self, value=None):
    if value is None:
      return self.d2
    self.d2 = value if isinstance(value, ByteValue) else \
      ByteValue(value)

  def set_fix_effective_address(self):
    self.fix_effective = True

  def should_fix_effective_address(self):
    ret_val = self.fix_effective
    if ret_val:
      self.fix_effective = False
    return ret_val
