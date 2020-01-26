class InstructionNode:

  def __init__(self, change_fxn, addressing_fxn, dest, pc_disp, cycles):
    self.change_fxn = change_fxn
    self.addressing_fxn = addressing_fxn
    self.dest_name = dest
    self.pc_disp = pc_disp
    self.cycles = cycles

  def set_operand1(self, system, operand):
    self.set_operand(system, operand, 1)

  def set_operand2(self, system, operand):
    self.set_operand(system, operand, 2)

  def set_operand(self, system, operand, operand_num):
    operand_name = "operand" + str(operand_num)
    if operand in system.cpu_registers():
      if operand == 'SP' and self.addressing_fxn is not None:
        operand_value, cycle_count = system.read(operand, self.addressing_fxn, self.cycles)
        setattr(self, operand_name, operand_value)
        self.cycles = cycle_count
      else:
        operand_value = system.read(operand)
        setattr(self, operand_name, operand_value)
    elif operand in system.status_flags():
      operand_value = system.status(operand)
      setattr(self, operand_name, operand_value)
    elif operand is not None:
      operand_value, cycle_count = system.read(operand, self.addressing_fxn, self.cycles)
      setattr(self, operand_name, operand_value)
      self.cycles = cycle_count
    else:
      setattr(self, operand_name, None)

  def metadata(self):
    return (
      self.operand1,
      self.operand2,
      self.dest_name
    )

  # def pc_metadata(self):
  #   return (
  #     self.pc_disp,
  #     self.cycles
  #   )

  def pc_metadata(self, system):
    return (
      self.operand1,
      self.operand2,
      system.cpu_register("PC"),
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
