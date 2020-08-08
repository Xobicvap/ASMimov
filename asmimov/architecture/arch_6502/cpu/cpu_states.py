from architecture.math.hexnum import WordValue, ByteValue

def increment_pc(cpu):
  cpu.pc(cpu.pc() + 1)
  cpu.pc().fix_page_boundaries()
  return cpu

################################################################
# PULL / PUSH / STACK OPERATIONS
################################################################

def increment_sp(cpu):
  cpu.sp(cpu.sp() + 1)
  return cpu, None

def decrement_sp(cpu):
  cpu.sp(cpu.sp() - 1)
  return cpu, None

def address_of_stack(cpu):
  cpu.address_set(cpu.sp().get_effective())
  return cpu

def push_pch_and_decrement_sp(cpu):
  """
  Remember, this is setting the address OF THE STACK on the bus
  then writing the high byte of the PC
  """
  cpu = address_of_stack(cpu)
  # this looks wrong initially but it's only writing a byte;
  # it's not writing an entire address
  cpu.address_write(cpu.pc().get_hi_byte())
  return decrement_sp(cpu)

def push_pcl_and_decrement_sp(cpu):
  # see comments for push_pch_and_decrement_sp
  cpu = address_of_stack(cpu)
  cpu.address_write(cpu.pc().get_lo_byte())
  return decrement_sp(cpu)

def pull_pcl_and_increment_sp(cpu):
  cpu = address_of_stack(cpu)
  cpu.pc().set_lo_byte(cpu.address_bus.read())
  cpu.address_write(ByteValue(0))
  return increment_sp(cpu)

def pull_pch(cpu):
  cpu = address_of_stack(cpu)
  cpu.pc().set_hi_byte(cpu.address_bus.read())
  cpu.address_write(ByteValue(0))
  # don't increment sp?
  # cpu, _ = increment_sp(cpu)
  # return cpu, True
  return cpu, True

def push_p_with_b_flag_and_decrement_sp(cpu):
  cpu = address_of_stack(cpu)
  p = cpu.p()
  p = p | 0b00110000
  cpu.address_write(p)
  return decrement_sp(cpu)

def pull_p_and_increment_sp(cpu):
  cpu = address_of_stack(cpu)
  v = cpu.address_bus.read()
  # bits 5 and 4 don't actually exist and have to be
  # read directly from the stack
  # in P they are never set
  v = v & 0b11001111
  cpu.p(v)
  cpu.address_write(ByteValue(0))
  return increment_sp(cpu)

def push_register_decrement_sp(cpu, register):
  v = cpu.register(register)
  cpu = address_of_stack(cpu)
  if register == "P":
    v = v | 0b00110000

  cpu.address_write(v)
  cpu, _ = decrement_sp(cpu)
  return cpu, True

def pull_register(cpu, register):
  cpu = address_of_stack(cpu)
  v = cpu.address_read()
  cpu.register(register, v)
  cpu.address_write(ByteValue(0))
  return cpu, True

################################################################
# READ OPERATIONS
################################################################

def read_irq_vector_lo(cpu):
  # yes it would be easier to do this in one line but
  # that's not technically how this works
  cpu.address_set(cpu.irq_vector())
  cpu.pc().set_lo_byte(cpu.address_read())
  return cpu, None

def read_irq_vector_hi(cpu):
  cpu.address_set(cpu.irq_vector(True))
  cpu.pc().set_hi_byte(cpu.address_read())
  return cpu, True

def read_next_and_throw_away(cpu):
  cpu.address_set(cpu.pc())
  _ = cpu.address_read()
  return cpu, None

def read_next_throw_away_inc_pc(cpu):
  cpu, _ = read_next_and_throw_away(cpu)
  cpu.pc(cpu.pc() + 1)
  cpu.pc().fix_page_boundaries()
  return cpu, None

def read_from_effective_fix_address(cpu):
  print(str(cpu.address_bus.memory.memory_banks[0]))
  cpu.address_bus.address_word.fix_page_boundaries()
  v = cpu.address_read()
  cpu.DR(v)

  return cpu, None

def read_from_effective_address(cpu):
  v = cpu.address_read()
  cpu.DR(v)
  return cpu, None

def read_effective_add_index(cpu, index):
  # not sure it does anything with this?
  cpu, _ = read_from_effective_address(cpu)
  # again, probably not accurate, but in service to
  # getting things done, meh
  cpu.address_set(cpu.address_bus.address_word + index)
  return cpu, None

def read_effective_add_x(cpu):
  return read_effective_add_index(cpu, cpu.x())

def read_effective_add_y(cpu):
  return read_effective_add_index(cpu, cpu.y())

def read_pointer_add_x(cpu):
  ptr = cpu.DR()
  ptr = ptr + cpu.x()
  cpu.DR(ptr)
  return cpu, None

################################################################
# FETCH OPERATIONS
################################################################

def copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch(cpu):
  """
  Kind of confusing...
  1. set the address bus (which should have been the stack if this is jsr)
     to the address of PC, which is PC + 2 from the start of the JMP/JSR
  2. read PC (= PC + 2) from the address bus to get intended PC high byte
  3. write word(pc lo, pc hi) to PC
  """
  cpu.address_set(cpu.pc())
  intended_pc_hi = cpu.address_read()
  intended_pc_lo = cpu.DR()
  pc_address = WordValue(intended_pc_lo, intended_pc_hi)
  cpu.pc(pc_address)

  return cpu, True

def fetch_instruction(cpu):
  cpu.address_set(cpu.pc())
  cpu = increment_pc(cpu)
  cpu.IR(cpu.address_read())
  return cpu, False

def fetch_value_and_increment_pc(cpu):
  cpu.address_set(cpu.pc())
  v = cpu.address_read()
  cpu.DR(v)
  cpu = increment_pc(cpu)
  return cpu, None

# absolute instructions
# this is identical to fetch_value_and_increment_pc apart from name
def fetch_address_lo_byte_increment_pc(cpu):
  cpu.address_set(cpu.pc())
  pcl = cpu.address_read()
  cpu.DR(pcl)
  cpu = increment_pc(cpu)
  return cpu, None

def fetch_address_hi_byte_increment_pc(cpu):
  cpu.address_set(cpu.pc())
  pch = cpu.address_read()
  address_word = WordValue(cpu.DR(), pch)
  cpu.address_set(address_word)
  cpu = increment_pc(cpu)
  return cpu, None

def fetch_pch_copy_to_pc(cpu):
  # don't increment past page
  current_address = cpu.address_bus.address_word
  current_lo = current_address.get_lo_byte()
  current_lo = current_lo + 1
  current_address.set_lo_byte(current_lo)

  cpu.address_set(current_address)
  pc_lo = cpu.DR()
  v = cpu.address_read()
  pc_address = WordValue(pc_lo, v)
  cpu.pc(pc_address)
  return cpu, True

# absolute indexed
def fetch_address_hi_byte_add_index_lo_increment_pc(cpu, index):
  cpu.address_set(cpu.pc())
  # this too is confusing; PC here is PC + 2 (high byte of absolute addr)
  # so what is read as pch is that; it reads the _byte that's there_, not
  # the high byte of the PC address itself
  # e.g. if PC(+2) = 8004 and fe is stored at 8004, that's what will become the
  pch = cpu.address_read()

  index.unsigned = True
  temp_addr = WordValue(cpu.DR() + index, pch)
  cpu.address_set(temp_addr)

  return increment_pc(cpu), None

def fetch_address_hi_byte_add_x_lo_increment_pc(cpu):
  return fetch_address_hi_byte_add_index_lo_increment_pc(cpu, cpu.x())

def fetch_address_hi_byte_add_y_lo_increment_pc(cpu):
  return fetch_address_hi_byte_add_index_lo_increment_pc(cpu, cpu.y())

def fetch_address_zero_page_increment_pc(cpu):
  cpu.address_set(cpu.pc())

  lo_byte = cpu.address_read()
  hi_byte = 0
  address_value = WordValue(lo_byte, hi_byte)
  cpu.address_set(address_value)
  return increment_pc(cpu), None

def fetch_indirect_effective_address_lo(cpu):
  # previous instruction fetched the pointer (the operand following the instruction)
  # into DR; now, turn this into a zero page address
  ptr = cpu.DR()
  address_value = WordValue(ptr.value, 0)
  # set the ZP address and read from it; i.e. lda ($80), y
  # means read from $0080 and put the value in D2
  cpu.address_set(address_value)
  v = cpu.address_read()
  cpu.D2(v)
  return cpu, None

def fetch_indirect_effective_address_hi_add_y(cpu):
  ptr = cpu.DR()
  address_value = WordValue(ptr.value + 1, 0)
  cpu.address_set(address_value)
  hi_byte_effective = cpu.address_read()
  cpu.DR(hi_byte_effective)

  temp = cpu.D2() + cpu.y()
  if temp.carry():
    cpu.set_fix_effective_address()
  cpu.D2(temp)
  return cpu, None

################################################################
# WRITE OPERATIONS
################################################################

def write_back_to_effective_address(cpu):
  v = cpu.DR()
  cpu.address_write(v)
  return cpu, None

def write_new_to_effective_address(cpu):
  cpu, _ = write_back_to_effective_address(cpu)
  return cpu, True

def write_register_to_effective_address(cpu, register):
  cpu.address_write(register)
  return cpu, True

def write_a_to_effective_address(cpu):
  return write_register_to_effective_address(cpu, cpu.a())

def write_x_to_effective_address(cpu):
  return write_register_to_effective_address(cpu, cpu.x())

def write_y_to_effective_address(cpu):
  return write_register_to_effective_address(cpu, cpu.y())

################################################################
# INDIRECT OPERATIONS
################################################################

def indexed_indirect_address_lo(cpu):
  address_value = WordValue(cpu.DR().value, 0)
  cpu.address_set(address_value)
  address_lo = cpu.address_read()
  # this isn't really what happens, but meh
  cpu.D2(address_lo)
  return cpu, None

def indexed_indirect_address_hi(cpu):
  cpu.DR(cpu.DR() + 1)
  address_value = WordValue(cpu.DR().value, 0)
  cpu.address_set(address_value)
  address_hi = cpu.address_read()
  address_value = WordValue(cpu.D2(), address_hi)
  cpu.address_set(address_value)
  return cpu, None

def indirect_indexed_read_and_fix(cpu):
  hi_byte = cpu.DR()
  lo_byte = cpu.D2()
  address_value = WordValue(lo_byte, hi_byte)
  cpu.address_set(address_value)
  temp = cpu.address_read()
  if cpu.should_fix_effective_address():
    cpu.DR(cpu.DR() + 1)
    return cpu, None
  cpu.DR(temp)
  return cpu, True


fetch_pointer_address_increment_pc = fetch_value_and_increment_pc





