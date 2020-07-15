from architecture.arch_6502.cpu.cpu_cycle_fxns import *

class SystemCPU:
  def __init__(self, cpu):
    self.cpu = cpu
    self.cycles = 0
    self.current_steps = []

  def determine_instruction(self):
    instructions = per_cycle_fxns(self.cpu.IR())
    self.current_steps = instructions

  def step(self):
    if len(self.current_steps) == 0:
      self.current_steps.append(fetch_instruction)
    current_inst = self.current_steps.pop(0)
    self.cpu, state = current_inst(self.cpu)
    # no, pycharm, it can't be simplified, state == None
    # means there are more instructions following
    if state is None:
      pass
    elif state:
      self.determine_instruction()
    elif not state:
      self.current_steps = []
    self.cycles = self.cycles + 1
