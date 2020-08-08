from architecture.arch_6502.cpu.cpu_cycle_fxns import *
from analysis.aggregator import Aggregator


class SystemCPU:
  def __init__(self, cpu, use_aggregator=False, aggregate_end_only=True):
    self.cpu = cpu
    self.cycles = 0
    self.current_steps = []
    self.aggregator = Aggregator("CPU", use_aggregator)
    self.aggregate_end_only = aggregate_end_only

  def determine_instruction(self):
    instructions = per_cycle_fxns[self.cpu.IR().value]
    self.current_steps = instructions

  def step(self):
    if len(self.current_steps) == 0:
      self.current_steps.append(fetch_instruction)
    current_inst = self.current_steps.pop(0)
    self.cpu, instruction_operating = current_inst(self.cpu)
    # no, pycharm, it can't be simplified, state == None
    # means there are more instructions following
    if instruction_operating is None:
      pass
    elif not instruction_operating:
      self.determine_instruction()
    elif instruction_operating:
      self.current_steps = []
    self.cycles = self.cycles + 1
    if self.aggregate_end_only:
      if instruction_operating is False:
        self.aggregator.aggregate(self.cycles, **self.cpu.change_map)
    else:
      self.aggregator.aggregate(self.cycles, **self.cpu.change_map)

