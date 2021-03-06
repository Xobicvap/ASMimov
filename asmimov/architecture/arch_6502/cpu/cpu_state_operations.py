from .cpu_states import *
from architecture.math.hexnum import WordValue,\
  DecimalByteValue, ByteValue

# wait... why bit set and not bit at? same thing
def compute_bit7_set(v):
  return 1 if v.bit_set(7) else 0

def compute_bit0_set(v):
  return 1 if v.bit_set(0) else 0

def compute_z(v):
  return 1 if v == 0 else 0

####################################################
# NO OPERATION
####################################################

def nop(cpu, implied=None):
  return cpu, True

####################################################
# PUSH / PULL
####################################################

# ALL of these are implied! the implied var here is a no-op
def php(cpu, implied=None):
  return push_register_decrement_sp(cpu, "P")

def pha(cpu, implied=None):
  return push_register_decrement_sp(cpu, "A")

def pla(cpu, implied=None):
  return pull_register(cpu, "A")

def plp(cpu, implied=None):
  return pull_register(cpu, "P")

####################################################
# FLAG MANIPULATION
####################################################

def clc(cpu, implied=None):
  cpu.c(0)
  return cpu, True

def sec(cpu, implied=None):
  cpu.c(1)
  return cpu, True

def cli(cpu, implied=None):
  cpu.i(0)
  return cpu, True

def sei(cpu, implied=None):
  cpu.i(1)
  return cpu, True

def clv(cpu, implied=None):
  cpu.v(1)
  return cpu, True

def cld(cpu, implied=None):
  cpu.d(0)
  return cpu, True

def sed(cpu, implied=None):
  cpu.d(1)
  return cpu, True

####################################################
# TRANSFER OPS
####################################################

def tax(cpu, implied=None):
  cpu.x(cpu.a())
  return cpu, True

def tay(cpu, implied=None):
  cpu.y(cpu.a())
  return cpu, True

def txa(cpu, implied=None):
  cpu.a(cpu.x())
  return cpu, True

def tya(cpu, implied=None):
  cpu.a(cpu.y())
  return cpu, True

def txs(cpu, implied=None):
  cpu.sp(cpu.x())
  return cpu, True

def tsx(cpu, implied=None):
  cpu.x(cpu.sp())
  return cpu, True

####################################################
# BRANCHING
####################################################

def branch(cpu, condition):
  if condition:
    offset = cpu.DR()
    temp_pc = cpu.pc() + offset

    if temp_pc.page_boundaries_crossed():
      cpu.pc(temp_pc)
      return cpu, None
    cpu.pc(temp_pc)
    return cpu, True
  #cpu = increment_pc(cpu)
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
  # in a RWM scenario the write here is valid.
  # not sure if that's true in an implied sense?
  # we'll find out! weeknights at 8!
  if implied:
    cpu.a(v)
  else:
    cpu.address_write(v)
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

def sbc(cpu):
  v = cpu.DR()
  a = cpu.a()

  if cpu.d() == 1:
    v = DecimalByteValue(v)
    a = DecimalByteValue(a)

  temp = a - v - cpu.c()
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

def increment(cpu, reg, name):
  reg = reg + 1
  cpu.n(reg.negative())
  cpu.z(reg.zero())
  cpu.register(name, reg)
  return cpu, True

def dec(cpu, implied=None):
  v = cpu.DR()
  v = v - 1
  cpu.n(v.negative())
  cpu.z(v.zero())
  cpu.DR(v)
  return cpu

def inc(cpu, implied=None):
  v = cpu.DR()
  v = v + 1
  cpu.n(v.negative())
  cpu.z(v.zero())
  cpu.DR(v)
  return cpu

def dey(cpu, implied=None):
  y = cpu.y()
  return decrement(cpu, y, "Y")

def dex(cpu, implied=None):
  x = cpu.x()
  return decrement(cpu, x, "X")

def iny(cpu, implied=None):
  y = cpu.y()
  return increment(cpu, y, "Y")

def inx(cpu, implied=None):
  x = cpu.x()
  return increment(cpu, x, "X")

####################################################
# READ / WRITE
####################################################

def sta(cpu):
  cpu, _ = write_a_to_effective_address(cpu)
  return cpu, True

def stx(cpu):
  cpu, _ = write_x_to_effective_address(cpu)
  return cpu, True

def sty(cpu):
  cpu, _ = write_y_to_effective_address(cpu)
  return cpu, True

def lda(cpu):
  cpu.a(cpu.DR())
  load_assign_status(cpu, cpu.a())
  return cpu, True

def ldx(cpu):
  cpu.x(cpu.DR())
  load_assign_status(cpu, cpu.x())
  return cpu, True

def ldy(cpu):
  cpu.y(cpu.DR())
  load_assign_status(cpu, cpu.y())
  return cpu, True

def load_assign_status(cpu, register):
  cpu.n(1) if register.negative() else cpu.n(0)
  cpu.z(1) if register.zero() else cpu.z(0)
  return cpu

####################################################
# COMPARISONS
####################################################

def bit_op(cpu):
  v = cpu.DR()
  a = cpu.a()
  v2 = a & v
  cpu.c(v2.zero())
  cpu.n(v.bit_at(7))
  cpu.v(v.bit_at(6))
  return cpu, True

def comparison(op1, op2, cpu):
  temp = op1 - op2
  carry = 1 if op1.value >= op2.value else 0
  zero = 1 if op1.value == op2.value else 0
  negative = 1 if temp.negative() else 0

  cpu.c(carry)
  cpu.z(zero)
  cpu.n(negative)
  return cpu, True

def cpy(cpu):
  v = cpu.DR()
  y = cpu.y()
  return comparison(y, v, cpu)

def cpx(cpu):
  v = cpu.DR()
  x = cpu.x()
  return comparison(x, v, cpu)

def cmp(cpu):
  v = cpu.DR()
  a = cpu.a()
  return comparison(a, v, cpu)

####################################################
# OPERATIONS CLASSES
####################################################

class OperationType:
  def __init__(self, operation=None):
    self.operation = operation

  def __str__(self):
    return self.operation.__name__ + ":" + self.__class__.__name__

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
    return self.operation(cpu, True)

class Immediate(OperationType):
  def __call__(self, cpu):
    cpu, _ = fetch_value_and_increment_pc(cpu)
    return self.operation(cpu)

# this last step of writes is never different
class WriteRegisterOperation(OperationType):
  def __call__(self, cpu):
    return self.operation(cpu)

class AbsoluteRead(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    return self.operation(cpu)

class AbsoluteReadModifyWrite(OperationType):
  def __call__(self, cpu):
    cpu, _ = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class AbsoluteReadX(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    if cpu.address_bus.address_word.fix_page_boundaries():
      return cpu, None
    return self.operation(cpu)

class AbsoluteReadModifyWriteX(OperationType):
  def __call__(self, cpu):
    cpu, _ = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class AbsoluteReadY(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    if cpu.address_bus.address_word.fix_page_boundaries():
      return cpu, None
    return self.operation(cpu)

class AbsoluteWriteY(OperationType):
  def __call__(self, cpu):
    cpu, _ = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class ZeroPageRead(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    return self.operation(cpu)

class ZeroPageReadModifyWrite(OperationType):
  def __call__(self, cpu):
    cpu, _ = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class ZeroPageReadX(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    return self.operation(cpu)

class ZeroPageReadModifyWriteX(OperationType):
  def __call__(self, cpu):
    cpu, _ = write_back_to_effective_address(cpu)
    cpu, _ = self.operation(cpu)
    return cpu, None

class ZeroPageReadY(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    return self.operation(cpu)

class IndexedIndirectRead(OperationType):
  def __call__(self, cpu):
    cpu, _ = read_from_effective_address(cpu)
    return self.operation(cpu)

class IndirectIndexedRead(OperationType):
  def __call__(self, cpu):
    cpu, state = indirect_indexed_read_and_fix(cpu)
    if state is None:
      return cpu, state
    return self.operation(cpu)

class IndirectIndexedWrite(OperationType):
  def __call__(self, cpu):
    return indirect_indexed_read_and_fix(cpu)










