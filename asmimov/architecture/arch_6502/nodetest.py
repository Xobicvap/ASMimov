from instructions import instruction_tuples

class System:

  def __init__(self):
    self.register_map = {
      "A": 0,
      "X": 0,
      "Y": 0,
      "PC": 0x400,
      "P": 0,
      "SP": 0x1ff
    }
    self.clock_cycles = 0
    # if setting this to 0, make None the appropriate instruction
    self.memory_map = {}
    self.program_space = {}
    for i in range(0, 0x10000):
      self.memory_map[i] = 0
      self.program_space[i] = None

  def status(self, flag=None):
    status_byte = self.register_map["P"]
    if flag is None:
      return status_byte

    if flag == "N":
      return status_byte & 0x80
    elif flag == "V":
      return status_byte & 0x40
    elif flag == "D":
      return status_byte & 0x08
    elif flag == "I":
      return status_byte & 0x04
    elif flag == "Z":
      return status_byte & 0x02
    elif flag == "C":
      return status_byte & 0x01
    else:
      raise Exception("Invalid status flag requested")

  def status_write(self, status_reg):
    try:
      dest_status = self.register_map["P"]
      for flag, status_bit in status_reg.items():
        if flag == "N":
          dest_status = dest_status | 0x80 if status_bit = 1 else dest_status & 0x7f
        elif flag == "V":
          dest_status = dest_status | 0x40 if status_bit = 1 else dest_status & 0xbf
        elif flag == "D":
          dest_status = dest_status | 0x08 if status_bit = 1 else dest_status & 0xf7
        elif flag == "I":
          dest_status = dest_status | 0x04 if status_bit = 1 else dest_status & 0xfb
        elif flag == "Z":
          dest_status = dest_status | 0x02 if status_bit = 1 else dest_status & 0xfd
        elif flag == "C":
          dest_status = dest_status | 0x01 if status_bit = 1 else dest_status & 0xfe
        else:
          raise Exception("Invalid status flag written")
      self.cpu_register('P', dest_status)
    except:
      self.cpu_register('P', status_reg)

  def cpu_registers(self):
    return self.register_map.keys()

  def cpu_register(self, reg, value=None):
    if value is None:
      return self.register_map[reg]
    self.register_map[reg] = value

  def read(self, operand, addr_fxn=None, cycles=None):
    if operand in self.cpu_registers():
      return self.cpu_register(operand)
    return addr_fxn(self.memory_map, operand, cycles)

  def read_direct(self, addr):
    return self.memory_map[addr]

  def write(self, memory_addr, val):
    self.memory_map[memory_addr] = val

  def push(self, stack_ptr, val):
    try:
      for v in val:
        self.write(stack_ptr, v)
        stack_ptr = stack_ptr - 1
    except TypeError:
      self.write(stack_ptr, v)
      stack_ptr = stack_ptr -1
    self.cpu_register("SP", stack_ptr)

  def pop(self, stack_ptr, num_bytes):
    for i in range(1, num_bytes + 1):
      stack_ptr = stack_ptr + 1
      self.write(stack_ptr, 0)
    self.cpu_register("SP", stack_ptr)

  def change(self, **change_map):
    for dest, val in change_map.items():
      if dest == "push":
        stack_ptr = self.cpu_register("SP")

      elif dest == "PC":
        self.cpu_register(dest, system.cpu_register(dest) + val)
      elif dest == "P":
        self.status_write(val)
      elif dest in ['A', 'X', 'Y']:
        self.cpu_register(dest, val)
      else:
        # figure out how we do I/O registers later
        self.write(dest, val)

class InstructionNode:

  def __init__(self, change_fxn, addressing_fxn, dest, pc_disp, cycles):
    self.change_fxn = change_fxn
    self.addressing_fxn = addressing_fxn
    self.dest_name = dest
    self.pc_disp = pc_disp
    self.cycles = cycles

  # use setattr instead and avoid duplication
  def set_operand1(self, system, operand):
    if operand in system.cpu_registers():
      self.operand1 = system.read(operand)
    else:
      self.operand1, self.cycles = system.read(operand, self.addressing_fxn, self.cycles)

  def set_operand2(self, system, operand):
    if operand in system.cpu_registers():
      self.operand2 = system.read(operand)
    else:
      self.operand2, self.cycles = system.read(operand, self.addressing_fxn, self.cycles)

  def metadata(self):
    return (
      self.operand1,
      self.operand2,
      self.dest_name
    )

  def pc_metadata(self):
    return (
      self.pc_disp,
      self.cycles
    )

  def evaluate(self, system):
    changes = self.change_fxn(system, self)
    if "PC" not in changes:
      changes["PC"] = system.cpu_register("PC") + self.pc_disp
    if "cycles" not in changes:
      changes["cycles"] = system.clock_cycles + self.cycles
    return changes


if __name__ == "__main__":
  system_6502 = System()
  system_6502.cpu_register('A', 5)
  system_6502.memory_map[0x10] = 0x40
  # 10000010 << = (c=1) 00000100
  system_6502.memory_map[0x11] = 0x82

  inst_data = instruction_tuples[0x06]
  operand = 0x10

  # put this in a function somewhere, probably the reader
  change_fxn, addr_fxn, operand1, operand2, dest, pc_disp, cycles = inst_data
  operand1 = operand if operand1 == "operand" else operand1
  operand2 = operand if operand2 == "operand" else operand2

  instruction = InstructionNode(change_fxn, addr_fxn, 0x10, pc_disp, cycles)
  # this syntax is still janky
  instruction.set_operand1(system_6502, operand1)
  instruction.set_operand2(system_6502, operand2)

  print(instruction.metadata())
  
  changes = instruction.evaluate(system_6502)
  print(changes)


  inst_data = instruction_tuples[0x05]
  operand = 0x10

  # put this in a function somewhere, probably the reader
  change_fxn, addr_fxn, operand1, operand2, dest, pc_disp, cycles = inst_data
  operand1 = operand if operand1 == "operand" else operand1
  operand2 = operand if operand2 == "operand" else operand2

  instruction = InstructionNode(change_fxn, addr_fxn, 0x10, pc_disp, cycles)
  # this syntax is still janky
  instruction.set_operand1(system_6502, operand1)
  instruction.set_operand2(system_6502, operand2)

  print(instruction.metadata())
  
  changes = instruction.evaluate(system_6502)
  print(changes)

