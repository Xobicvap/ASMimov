from architecture.math.hexnum import WordValue

def increment_pc(cpu):
  cpu.pc(cpu.pc() + 1)
  return cpu

def address_of_stack(cpu):
  cpu.address_bus.set(cpu.sp().get_effective())
  return cpu

def fetch_instruction(cpu):
  cpu.address_bus.set(cpu.pc())
  cpu, _ = increment_pc(cpu)
  cpu.IR(cpu.address_bus.read())
  cpu.states = cpu.determine_instruction(cpu.IR())
  return cpu, None

def read_next_and_throw_away(cpu):
  cpu.address_bus.set(cpu.pc())
  _ = cpu.address_bus.read()
  return cpu, None

def read_next_throw_away_inc_pc(cpu):
  cpu, _ = read_next_and_throw_away(cpu)
  cpu.pc(cpu.pc() + 1)
  return cpu, None

def increment_sp(cpu):
  cpu.sp(cpu.sp() + 1)
  return cpu, None

def decrement_sp(cpu):
  cpu.sp(cpu.sp() - 1)
  return cpu, None

def push_pch_and_decrement_sp(cpu):
  """
  Remember, this is setting the address OF THE STACK on the bus
  then writing the high byte of the PC
  :param cpu:
  :return: state tuple
  """
  cpu = address_of_stack(cpu)
  cpu.address_bus.write(cpu.pc().get_hi_byte())
  return decrement_sp(cpu)

def push_pcl_and_decrement_sp(cpu):
  # see comments for push_pch_and_decrement_sp
  cpu = address_of_stack(cpu)
  cpu.address_bus.write(cpu.pc().get_lo_byte())
  return decrement_sp(cpu)

def pull_pcl_and_increment_sp(cpu):
  cpu = address_of_stack(cpu)
  cpu.pc().set_lo_byte(cpu.address_bus.read())
  cpu.address_bus.write(0)
  return increment_sp(cpu)

def pull_pch(cpu):
  cpu = address_of_stack(cpu)
  cpu.pc().set_hi_byte(cpu.address_bus.read())
  cpu.address_bus.write(0)
  # don't increment sp?
  # cpu, _ = increment_sp(cpu)
  # return cpu, True
  return cpu, True

def push_p_with_b_flag_and_decrement_sp(cpu):
  cpu = address_of_stack(cpu)
  p = cpu.p()
  p = p | 0b00110000
  cpu.address_bus.write(p)
  return decrement_sp(cpu)

def read_irq_vector_lo(cpu):
  # yes it would be easier to do this in one line but
  # that's not technically how this works
  cpu.address_bus.set(cpu.irq_vector.get_lo_byte())
  cpu.pc().set_lo_byte(cpu.address_bus.read())
  return cpu, None

def read_irq_vector_hi(cpu):
  cpu.address_bus.set(cpu.irq_vector.get_hi_byte())
  cpu.pc().set_hi_byte(cpu.address_bus.read())
  return cpu, True

def pull_p_and_increment_sp(cpu):
  cpu = address_of_stack(cpu)
  cpu.p(cpu.address_bus.read())
  cpu.address_bus.write(0)
  return increment_sp(cpu)

def push_register_decrement_sp(cpu, register):
  v = cpu.register(register)
  cpu = address_of_stack(cpu)
  cpu.address_bus.write(v)
  cpu, _ = decrement_sp(cpu)
  return cpu, True

def pull_register(cpu, register):
  v = cpu.address_bus.read()
  cpu.register(register, v)
  return cpu, True

def fetch_value_and_increment_pc(cpu):
  cpu.address_bus.set(cpu.pc())
  v = cpu.address_bus.read()
  cpu.DR(v)
  return increment_pc(cpu)

def copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch(cpu):
  cpu.address_bus.set(cpu.pc())
  pch = cpu.address_bus.read()
  cpu.address_bus.read().set_lo_byte(cpu.DR())
  cpu.address_bus.read().set_hi_byte(pch)
  cpu.pc().write(cpu.address_bus.read())
  return cpu, True

# absolute instructions
def fetch_address_lo_byte_increment_pc(cpu):
  cpu.address_bus.set(cpu.pc())
  pcl = cpu.address_bus.read()
  cpu.address_bus.read().set_lo_byte(pcl)
  return increment_pc(cpu)

def fetch_address_hi_byte_increment_pc(cpu):
  cpu.address_bus.set(cpu.pc())
  pch = cpu.address_bus.read()
  cpu.address_bus.read().set_hi_byte(pch)
  return increment_pc(cpu)

# absolute indexed
def fetch_address_hi_byte_add_index_lo_increment_pc(cpu, index):
  cpu.address_bus.set(cpu.pc())
  pch = cpu.address_bus.read()
  cpu.address_bus.read().set_hi_byte(pch)
  index.unsigned = True
  temp_addr = WordValue(cpu.address_bus.address) + index
  cpu.address_bus.set(temp_addr)

  return increment_pc(cpu)

def fetch_address_hi_byte_add_x_lo_increment_pc(cpu):
  return fetch_address_hi_byte_add_index_lo_increment_pc(cpu.x())

def fetch_address_hi_byte_add_y_lo_increment_pc(cpu):
  return fetch_address_hi_byte_add_index_lo_increment_pc(cpu.y())

def read_from_effective_fix_address(cpu):
  v = cpu.address_bus.read()
  cpu.DR(v)
  cpu.address_bus.address_word.fix_page_boundaries()
  return cpu, None

def fetch_address_zero_page_increment_pc(cpu):
  cpu.address_bus.set(cpu.pc())
  # not sure i like this syntax
  lo_byte = cpu.address_bus.read().value
  hi_byte = 0
  address_value = WordValue(lo_byte, hi_byte)
  cpu.address_bus.set(address_value)
  return increment_pc(cpu)

def read_from_effective_address(cpu):
  v = cpu.address_bus.read()
  cpu.DR(v)
  return cpu, None

def read_effective_add_index(cpu, index):
  # not sure it does anything with this?
  cpu = read_from_effective_address(cpu)
  # again, probably not accurate, but in service to
  # getting things done, meh
  cpu.address_bus.set(cpu.address_bus.address_word + index)
  return cpu, None

def read_effective_add_x(cpu):
  return read_effective_add_index(cpu, cpu.x())

def read_effective_add_y(cpu):
  return read_effective_add_index(cpu, cpu.y())

def write_back_to_effective_address(cpu):
  v = cpu.DR()
  cpu.address_bus.write(v)
  return cpu, None

def write_new_to_effective_address(cpu):
  cpu, _ = write_back_to_effective_address(cpu)
  return cpu, True

def write_register_to_effective_address(cpu, register):
  cpu.address_bus.write(register)
  return cpu, True

def write_a_to_effective_address(cpu):
  return write_register_to_effective_address(cpu, cpu.a())

def write_x_to_effective_address(cpu):
  return write_register_to_effective_address(cpu, cpu.x())

def write_y_to_effective_address(cpu):
  return write_register_to_effective_address(cpu, cpu.y())

def read_pointer_add_x(cpu):
  ptr = cpu.DR()
  ptr = ptr + cpu.x()
  cpu.DR(ptr)
  return cpu, None

def fetch_indirect_effective_address_lo(cpu):
  # previous instruction fetched the pointer (the operand following the instruction)
  # into DR; now, turn this into a zero page address
  ptr = cpu.DR()
  address_value = WordValue(ptr.value, 0)
  # set the ZP address and read from it; i.e. lda ($80), y
  # means read from $0080 and put the value in D2
  cpu.address_bus.set(address_value)
  v = cpu.address_bus.read()
  cpu.D2(v)
  return cpu, None

def fetch_indirect_effective_address_hi_add_y(cpu):
  ptr = cpu.DR()
  address_value = WordValue(ptr.value + 1, 0)
  cpu.address_bus.set(address_value)
  hi_byte_effective = cpu.address_bus.read()
  cpu.DR(hi_byte_effective)

  temp = cpu.D2() + cpu.y()
  if temp.carry():
    cpu.set_fix_effective_address()
  cpu.D2(temp)
  return cpu, None

def indexed_indirect_address_lo(cpu):
  address_value = WordValue(cpu.DR().value, 0)
  cpu.address_bus.set(address_value)
  address_lo = cpu.address_bus.read()
  # this isn't really what happens, but meh
  cpu.D2(address_lo)
  return cpu, None

def indexed_indirect_address_hi(cpu):
  cpu.DR(cpu.DR() + 1)
  address_value = WordValue(cpu.DR().value, 0)
  cpu.address_bus.set(address_value)
  address_hi = cpu.address_bus.read()
  address_value = WordValue(cpu.D2().value, address_hi)
  cpu.address_bus.set(address_value)
  return cpu, None

def indexed_indirect_read_and_fix(cpu):
  hi_byte = cpu.DR()
  lo_byte = cpu.D2()
  address_value = WordValue(lo_byte, hi_byte)
  cpu.address_bus.set(address_value)
  temp = cpu.address_bus.read()
  if cpu.should_fix_effective_address():
    cpu.DR(cpu.DR() + 1)
    return cpu, None
  cpu.DR(temp)
  return cpu, True


fetch_pointer_address_increment_pc = fetch_value_and_increment_pc





