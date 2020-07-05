
def increment_pc(cpu):
  cpu.pc(cpu.pc() + 1)
  return cpu

def address_of_stack(cpu):
  cpu.address_bus.set(cpu.sp().get_effective())
  return cpu

def fetch_instruction(cpu):
  cpu.address_bus.set(cpu.pc().get())
  cpu, _ = increment_pc(cpu)
  cpu.IR(cpu.address_bus.read())
  cpu.states = cpu.determine_instruction(cpu.IR())
  return cpu, None

def read_next_and_throw_away(cpu):
  cpu.address_bus.set(cpu.pc().get())
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
  cpu = address_of_stack(cpu)
  cpu.address_bus.write(cpu.pc().get_hi_byte())
  return decrement_sp(cpu)

def push_pcl_and_decrement_sp(cpu):
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
  cpu.address_bus.set(cpu.sp() + 0x100)
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
  cpu.address_bus.set(cpu.pc().get())
  pch = cpu.address_bus.read()
  cpu.address_bus.read().set_lo_byte(cpu.DR())
  cpu.address_bus.read().set_hi_byte(pch)
  cpu.pc().write(cpu.address_bus.read())
  return cpu, True

# absolute instructions
def fetch_address_lo_byte_increment_pc(cpu):
  cpu.address_bus.set(cpu.pc().get())
  pcl = cpu.address_bus.read()
  cpu.address_bus.read().set_lo_byte(pcl)
  return increment_pc(cpu)

def fetch_address_hi_byte_increment_pc(cpu):
  cpu.address_bus.set(cpu.pc().get())
  pch = cpu.address_bus.read()
  cpu.address_bus.read().set_hi_byte(pch)
  return increment_pc(cpu)

def read_from_effective_address(cpu):
  v = cpu.address_bus.read()
  cpu.DR(v)
  return cpu, None

def implied(cpu, operation):
  read_next_and_throw_away(cpu)
  return operation(cpu, None), True




