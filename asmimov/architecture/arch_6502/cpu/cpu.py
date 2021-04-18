from .address_bus import AddressBus
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

  def reset(self, override_reset=None):
    if override_reset is not None:
      self.pc(override_reset)
    else:
      lo_reset = self.reset_vector()
      hi_reset = self.reset_vector(True)
      self.address_set(lo_reset)
      reset_addr_lo = self.address_read()
      self.address_set(hi_reset)
      reset_addr_hi = self.address_read()
      reset_addr = WordValue(reset_addr_lo, reset_addr_hi)
      self.pc(reset_addr)

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

  def address_write(self, value):
    self.address_bus.write(value)
    self.write_change(self.address_bus.address_word.value, value)

  def address_read(self):
    return self.address_bus.read()

  def address_set(self, address):
    self.address_bus.set(address)

  def set_fix_effective_address(self):
    self.fix_effective = True

  def should_fix_effective_address(self):
    ret_val = self.fix_effective
    if ret_val:
      self.fix_effective = False
    return ret_val

  def collect_state(self):
    pc = str(self.pc())
    n = str(self.n())
    v = str(self.v())
    d = str(self.d())
    i = str(self.i())
    z = str(self.z())
    c = str(self.c())
    a = str(self.a())
    x = str(self.x())
    y = str(self.y())
    p = str(self.p())
    sp = str(self.sp())
    ir = str(self.IR())
    dr = str(self.DR())
    d2 = str(self.D2())
    return {
      "PC": pc,
      "N": n,
      "V": v,
      "D": d,
      "I": i,
      "Z": z,
      "C": c,
      "A": a,
      "X": x,
      "Y": y,
      "P": p,
      "SP": sp,
      "IR": ir,
      "DR": dr,
      "D2": d2
    }
