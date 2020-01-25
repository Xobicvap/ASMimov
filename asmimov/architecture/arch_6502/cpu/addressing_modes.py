def STACK_PTR_DISPLACEMENT_POP():
  return 0x101

def pop_byte(cpu_container, operand, cycles=None):
  # don't do the stack_pointer displacement here so we can 
  # track it in changes
  stack_ptr = cpu_container.cpu_register(operand)
  stack_ptr = stack_ptr + STACK_PTR_DISPLACEMENT_POP()
  return cpu_container.read_direct(stack_ptr)

def pop_word(cpu_container, operand, cycles=None):
  stack_ptr = cpu_container.cpu_register(operand)
  stack_ptr = stack_ptr + STACK_PTR_DISPLACEMENT_POP()
  addr_lo = cpu_container.read_direct(stack_ptr)
  addr_hi = cpu_container.read_direct(stack_ptr+1)

  return (addr_lo, addr_hi)

def pop_addr(cpu_container, operand, cycles=None):
  addr_lo, addr_hi = pop_word(cpu_container, operand, cycles)
  addr = 0
  addr_hi_word = addr_hi << 8
  addr = addr_hi_word + addr_lo
  return addr

def immediate(cpu_container, operand, cycles):
  return (operand, cycles)


relative = immediate


def indirect(cpu_container, operand, cycles):
  operand_lo = operand & 0xff
  addr_lo = cpu_container.read_direct(operand)
  if operand_lo == 0xff:
    addr_hi = cpu_container.read_direct(operand - 0xff)
  else:
    addr_hi = cpu_container.read_direct(operand + 1)

  addr_hi_word = addr_hi << 8
  return (addr_hi_word + addr_lo, cycles)

def indexed_indirect(cpu_container, operand, cycles):
  indexed = operand + cpu_container.cpu_register('X') & 0xff
  addr_hi = (cpu_container.read_direct(indexed + 1)) << 8
  addr_lo = cpu_container.read_direct(indexed)
  addr = addr_hi + addr_lo
  return (cpu_container.read_direct(addr), cycles)

def indirect_indexed(cpu_container, operand, cycles):
  y = cpu_container.cpu_register('Y')
  addr_lo = cpu_container.read_direct(operand) + y
  addr_hi = cpu_container.read_direct(operand + 1) << 8

  if addr_lo >= 0x100:
    addr_lo = addr_lo & 0xff
    cycles = cycles + 1
  addr = addr_hi + addr_lo
  return (cpu_container.read_direct(addr), cycles)

def direct(cpu_container, operand, cycles):
  return (cpu_container.read_direct(operand), cycles)

def zero_page(cpu_container, operand, cycles):
  return direct(cpu_container, operand, cycles)

def absolute(cpu_container, operand, cycles):
  return direct(cpu_container, operand, cycles)

def absolute_indexed(cpu_container, operand, cycles, v):
  lo_byte = operand & 0xff
  if v + lo_byte >= 0x100:
    cycles = cycles + 1
    hi_byte = operand & 0xff00
    # this might be off by 1
    addr = ((v + lo_byte) & 0xff) + hi_byte
  else:
    addr = operand + v
  return (cpu_container.read_direct(addr), cycles)

def absolute_x(cpu_container, operand, cycles):
  return absolute_indexed(cpu_container, operand, cycles, cpu_container.cpu_register('X'))

def absolute_y(cpu_container, operand, cycles):
  return absolute_indexed(cpu_container, operand, cycles, cpu_container.cpu_register('Y'))

def zero_page_indexed(cpu_container, operand, cycles, v):
  if v + operand >= 0x100:
    cycles = cycles + 1
    addr = ((v + operand) & 0xff)
  else:
    addr = operand + v
  return (cpu_container.read_direct(addr), cycles)

def zero_page_x(cpu_container, operand, cycles):
  return zero_page_indexed(cpu_container, operand, cycles, cpu_container.cpu_register('X'))

def zero_page_y(cpu_container, operand, cycles):
  return zero_page_indexed(cpu_container, operand, cycles, cpu_container.cpu_register('Y'))
