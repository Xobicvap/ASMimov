from .cpu_states import *
from architecture.arch_6502.math.hexnum import WordValue,\
  DecimalByteValue, ByteValue

# wait... why bit set and not bit at? same thing
def compute_bit7_set(v):
  return 1 if v.bit_set(7) else 0

def compute_bit0_set(v):
  return 1 if v.bit_set(0) else 0

def compute_z(v):
  return 1 if v == 0 else 0

####################################################
# PUSH / PULL
####################################################

def php(cpu):
  return push_register_decrement_sp(cpu, "P")

def pha(cpu):
  return push_register_decrement_sp(cpu, "A")

def pla(cpu):
  return pull_register(cpu, "A")

def plp(cpu):
  return pull_register(cpu, "P")

####################################################
# FLAG MANIPULATION
####################################################

def clc(cpu):
  cpu.c(0)
  return cpu, True

def sec(cpu):
  cpu.c(1)
  return cpu, True

def cli(cpu):
  cpu.i(0)
  return cpu, True

def sei(cpu):
  cpu.i(1)
  return cpu, True

def clv(cpu):
  cpu.v(1)
  return cpu, True

def cld(cpu):
  cpu.d(0)
  return cpu, True

def sed(cpu):
  cpu.d(1)
  return cpu, True

####################################################
# TRANSFER OPS
####################################################

def tax(cpu):
  cpu.x(cpu.a())
  return cpu, True

def tay(cpu):
  cpu.y(cpu.a())
  return cpu, True

def txa(cpu):
  cpu.a(cpu.x())
  return cpu, True

def tya(cpu):
  cpu.a(cpu.y())
  return cpu, True

def txs(cpu):
  cpu.sp(cpu.x())
  return cpu, True

def tsx(cpu):
  cpu.x(cpu.sp())
  return cpu, True

####################################################
# BRANCHING
####################################################

def branch(cpu, condition):
  if condition:
    offset = cpu.DR()
    temp_pc = cpu.pc() + offset

    if temp_pc.page_boundaries_crossed:
      return cpu, None
    return cpu, True
  cpu = increment_pc(cpu)
  return cpu, True

def bpl(cpu):
  return branch(cpu, cpu.n() == 0)

def bmi(cpu):
  return branch(cpu, cpu.n() == 1)

def bvc(cpu):
  return branch(cpu, cpu.v() == 0)

def bvs(cpu):
  return branch(cpu, cpu.v() == 1)

def bcc(cpu):
  return branch(cpu, cpu.c() == 0)

def bcs(cpu):
  return branch(cpu, cpu.c() == 1)

def bne(cpu):
  return branch(cpu, cpu.z() == 0)

def beq(cpu):
  return branch(cpu, cpu.z() == 1)

####################################################
# SHIFT / ROTATE
####################################################

def post_shift(cpu, implied, v):
  if implied:
    cpu.a(v)
  else:
    cpu.address_bus.write(v)
  cpu.n(v.negative())
  cpu.z(v.zero())
  return cpu

def asl(cpu, implied=False):
  v = cpu.a() if implied else cpu.DR()

  cpu.c(compute_bit7_set(v))
  v = v << 1
  cpu = post_shift(cpu, implied, v)
  return cpu, True

def rol(cpu, implied=False):
  v = cpu.a() if implied else cpu.DR()
  current_carry = cpu.c()
  cpu.c(compute_bit7_set(v))

  v = v << 1
  v = v if current_carry == 0 else v | 1
  cpu = post_shift(cpu, implied, v)
  return cpu, True

def lsr(cpu, implied=False):
  v = cpu.a() if implied else cpu.DR()

  cpu.c(compute_bit0_set(v))
  v = v >> 1
  cpu = post_shift(cpu, implied, v)
  return cpu, True

def ror(cpu, implied=False):
  v = cpu.a() if implied else cpu.DR()
  current_carry = cpu.c()
  cpu.c(compute_bit0_set(v))

  v = v << 1
  v = v if current_carry == 0 else v | 0x80
  cpu = post_shift(cpu, implied, v)
  return cpu, True

####################################################
# LOGICAL OPS
####################################################

def post_logical_ops(cpu, v2):
  cpu.n(v2.negative())
  cpu.z(v2.zero())
  cpu.a(v2)
  return cpu, True

def ora(cpu):
  v = cpu.DR()
  a = cpu.a()
  v2 = a | v
  return post_logical_ops(cpu, v2)

def eor(cpu):
  v = cpu.DR()
  a = cpu.a()
  v2 = a ^ v
  return post_logical_ops(cpu, v2)

def logical_and(cpu):
  v = cpu.DR()
  a = cpu.a()
  v2 = a & v
  return post_logical_ops(cpu, v2)

def bit_op(cpu):
  v = cpu.DR()
  a = cpu.a()
  v2 = a & v
  cpu.c(v2.zero())
  cpu.n(v.bit_set(7))
  cpu.v(v.bit_set(6))
  return cpu, True

####################################################
# ADD / SUBTRACT / INC / DEC
####################################################

def adc(cpu):
  v = cpu.DR()
  a = cpu.a()

  if cpu.d() == 1:
    v = DecimalByteValue(v)
    a = DecimalByteValue(a)

  temp = a + v + cpu.c()
  cpu.c(temp.carry())
  cpu.a(ByteValue(temp))
  cpu.v(temp.overflow())
  cpu.z(temp.zero())
  cpu.n(temp.negative())
  return cpu, True


def decrement(cpu, reg, name):
  reg = reg - 1
  cpu.n(reg.negative())
  cpu.z(reg.zero())
  cpu.register(name, reg)
  return cpu, True

def dey(cpu):
  y = cpu.y()
  return decrement(cpu, y, "Y")

def dex(cpu):
  x = cpu.x()
  return decrement(cpu, x, "X")

####################################################
# READ / WRITE
####################################################

def sta(cpu):
  cpu = write_a_to_effective_address(cpu)
  return cpu, True

def stx(cpu):
  cpu = write_x_to_effective_address(cpu)
  return cpu, True

def sty(cpu):
  cpu = write_y_to_effective_address(cpu)
  return cpu, True

####################################################
# OPERATIONS CLASSES
####################################################

class OperationType:
  def __init__(self, operation=None):
    self.operation = operation

class Relative(OperationType):
  def __call__(self, cpu):
    pc = cpu.pc()
    if pc.fix_page_boundaries():
      cpu.pc(pc)
      cpu.pc().reset_page_boundaries()
      return cpu, True
    return self.operation(cpu)

class Implied(OperationType):
  def __call__(self, cpu):
    cpu = read_next_and_throw_away(cpu)
    return self.operation(cpu, True)

class Immediate(OperationType):
  def __call__(self, cpu):
    cpu = fetch_value_and_increment_pc(cpu)
    return self.operation(cpu)

# this last step of writes is never different
class WriteRegisterOperation(OperationType):
  def __call__(self, cpu):
    return self.operation(cpu)

class AbsoluteRead(OperationType):
  def __call__(self, cpu):
    cpu = read_from_effective_address(cpu)
    return self.operation(cpu)

class AbsoluteReadModifyWrite(OperationType):
  def __call__(self, cpu):
    cpu = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class AbsoluteReadX(OperationType):
  def __call__(self, cpu):
    cpu = read_from_effective_address(cpu)
    if cpu.address_bus.address_word.fix_page_boundaries():
      return cpu, None
    return self.operation(cpu)

class AbsoluteReadModifyWriteX(OperationType):
  def __call__(self, cpu):
    cpu = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class AbsoluteReadY(OperationType):
  def __call__(self, cpu):
    cpu = read_from_effective_address(cpu)
    if cpu.address_bus.address_word.fix_page_boundaries():
      return cpu, None
    return self.operation(cpu)

class AbsoluteWriteY(OperationType):
  def __call__(self, cpu):
    cpu = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class ZeroPageRead(OperationType):
  def __call__(self, cpu):
    cpu = read_from_effective_address(cpu)
    return self.operation(cpu)

class ZeroPageReadModifyWrite(OperationType):
  def __call__(self, cpu):
    cpu = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class ZeroPageReadX(OperationType):
  def __call__(self, cpu):
    cpu = read_from_effective_address(cpu)
    return self.operation(cpu)

class ZeroPageReadModifyWriteX(OperationType):
  def __call__(self, cpu):
    cpu = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class IndexedIndirectRead(OperationType):
  def __call__(self, cpu):
    cpu = read_from_effective_address(cpu)
    return self.operation(cpu)

class IndirectIndexedRead(OperationType):
  def __call__(self, cpu):
    cpu, state = indexed_indirect_read_and_fix(cpu)
    if state is None:
      return cpu, state
    return self.operation(cpu)

class IndirectIndexedWrite(OperationType):
  def __call__(self, cpu):
    return indexed_indirect_read_and_fix(cpu)










