def STACK_PTR_DISPLACEMENT_POP():
  return 0x101

def pop_byte(system, operand, cycles):
  # don't do the stack_pointer displacement here so we can 
  # track it in changes
  stack_ptr = system.cpu_register(operand)
  stack_ptr = stack_ptr + STACK_PTR_DISPLACEMENT_POP()
  return system.read_direct(stack_ptr)

def pop_word(system, operand, cycles):
  stack_ptr = system.cpu_register(operand)
  stack_ptr = stack_ptr + STACK_PTR_DISPLACEMENT_POP()
  addr_lo = system.read_direct(stack_ptr)
  addr_hi = system.read_direct(stack_ptr+1)

  return (addr_lo, addr_hi)

def pop_addr(system, operand, cycles):
  addr_lo, addr_hi = pop_word(system, operand, cycles)
  addr = 0
  addr_hi_word = addr_hi << 8
  addr = addr_hi_word + addr_lo
  return addr

def immediate(system, operand, cycles):
  return operand

def branch_offset(system, operand, cycles):
  branch_disp = operand if operand < 0x80 else 0x100 - operand
  # determine cycle time
  return (branch_disp, cycles)

def indirect(system, operand, cycles):
  addr_lo = system.read_direct(operand)
  addr_hi = system.read_direct(operand + 1)

  addr_hi_word = addr_hi << 8
  return addr_hi_word + addr_lo


def indexed_indirect(system, operand, cycles):
  indexed = operand + system.cpu_register('X') & 0xff
  addr_hi = (indexed + 1) * 0x100
  addr_lo = indexed
  addr = addr_hi + addr_lo
  return (system.read_direct(addr), cycles)

def indirect_indexed(system, operand, cycles):
  y = system.cpu_register('Y')
  addr_lo = system.read_direct(operand) + y
  addr_hi = system.read_direct(operand + 1)
  if addr_lo > 0x100:
    addr_lo = addr_lo & 0xff
  addr = addr_hi + addr_lo
  return (system.read_direct(addr), cycles)

def direct(system, operand, cycles):
  return (system.read_direct(operand), cycles)

def zero_page(system, operand, cycles):
  return direct(system, operand, cycles)

def absolute(system, operand, cycles):
  return direct(system, operand, cycles)

def absolute_indexed(system, operand, cycles, v):
  lo_byte = operand & 0xff
  if v + lo_byte > 0x100:
    cycles = cycles + 1
    hi_byte = operand & 0xff00
    # this might be off by 1
    addr = ((v + lo_byte) & 0xff) + hi_byte
  else:
    addr = operand + v
  return (system.read_direct(addr), cycles)

def absolute_x(system, operand, cycles):
  return absolute_indexed(system, operand, cycles, system.cpu_register('X'))

def absolute_y(system, operand, cycles):
  return absolute_indexed(system, operand, cycles, system.cpu_register('Y'))

def zero_page_indexed(system, operand, cycles, v):
  if v + operand > 0x100:
    cycles = cycles + 1
    addr = ((v + operand) & 0xff)
  else:
    addr = operand + v
  return (system.read_direct(addr), cycles)

def zero_page_x(system, operand, cycles):
  return zero_page_indexed(system, operand, cycles, system.cpu_register('X'))

def zero_page_y(system, operand, cycles):
  return zero_page_indexed(system, operand, cycles, system.cpu_register('Y'))
