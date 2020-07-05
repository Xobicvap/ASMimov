from random import randrange

def set_memory_map_byte():
  return randrange(0, 0x100)


class CPUContainer:
  """
  Yeah, it's called a "CPU container" even though it also contains memory.
  If you have a better name, I'm all ears...

  By default, initialize everything randomly. For testing, allow for specific
  registers and memory to be set.
  """
  def __init__(self, a=None, x=None, y=None, pc=None, p=None, sp=None, memory={}):
    a = set_memory_map_byte() if a is None else a
    x = set_memory_map_byte() if x is None else x
    y = set_memory_map_byte() if y is None else y
    pc = 0x400 if pc is None else pc
    p = 0 if p is None else p
    sp = set_memory_map_byte() if sp is None else sp
    self.register_map = {
      "A": a,
      "X": x,
      "Y": y,
      "PC": pc,
      "P": p,
      "SP": sp
    }

    self.clock_cycles = 0

    # this is irrelevant
    self.program_space = {}

    self.vectors = {
      "IRQ/BRK": 0xfffe,
      "RESET": 0xfffc,
      "NMI": 0xfffa
    }

    # this gets set to random bytes because that's how the real world works
    if len(memory) == 0:
      for i in range(0, 0x10000):
        memory[i] = 0
    self.memory_map = memory

  def status(self, flag=None):
    status_byte = self.register_map["P"]
    if flag is None:
      return status_byte

    if flag == "N":
      return 1 if status_byte & 0x80 == 0x80 else 0
    elif flag == "V":
      return 1 if status_byte & 0x40 == 0x40 else 0
    elif flag == "D":
      return 1 if status_byte & 0x08 == 0x08 else 0
    elif flag == "I":
      return 1 if status_byte & 0x04 == 0x04 else 0
    elif flag == "Z":
      return 1 if status_byte & 0x02 == 0x02 else 0
    elif flag == "C":
      return 1 if status_byte & 0x01 == 0x01 else 0
    else:
      raise Exception("Invalid status flag requested")

  def status_write(self, status_reg):
    dest_status = self.register_map["P"]
    for flag, status_bit in status_reg.items():
      if flag == "N":
        dest_status = dest_status | 0x80 if status_bit == 1 else dest_status & 0x7f
      elif flag == "V":
        dest_status = dest_status | 0x40 if status_bit == 1 else dest_status & 0xbf
      elif flag == "D":
        dest_status = dest_status | 0x08 if status_bit == 1 else dest_status & 0xf7
      elif flag == "I":
        dest_status = dest_status | 0x04 if status_bit == 1 else dest_status & 0xfb
      elif flag == "Z":
        dest_status = dest_status | 0x02 if status_bit == 1 else dest_status & 0xfd
      elif flag == "C":
        dest_status = dest_status | 0x01 if status_bit == 1 else dest_status & 0xfe
      else:
        raise Exception("Invalid status flag written")
      self.cpu_register('P', dest_status)

  def cpu_registers(self):
    return self.register_map.keys()

  def status_flags(self):
    return ["N", "V", "D", "I", "Z", "C"]

  def cpu_register(self, reg, value=None):
    if value is None:
      return self.register_map[reg]
    self.register_map[reg] = value

  def read(self, operand, addr_fxn=None, cycles=None):
    if operand in self.cpu_registers():
      return self.cpu_register(operand)
    return addr_fxn(self, operand, cycles)

  def read_direct(self, addr):
    return self.memory_map[addr]

  def read_absolute_address(self, addr):
    addr_byte_lo = self.read_direct(addr)
    addr_byte_hi = self.read_direct(addr + 1)

    return (addr_byte_hi << 8) + addr_byte_lo

  def write(self, memory_addr, val):
    self.memory_map[memory_addr] = val

  def vector(self, name):
    return self.read_absolute_address(self.vectors[name])

  def change(self, **change_map):
    for dest, val in change_map.items():
      if dest == "P":
        self.status_write(val)
      elif dest in ['A', 'X', 'Y', 'SP', 'PC']:
        self.cpu_register(dest, val)
      else:
        # i/o isn't part of this, this is pure oldcpu, so no worries
        self.write(dest, val)
