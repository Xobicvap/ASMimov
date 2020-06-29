from .memory_bank import MemoryBank
from .soft_switches import SoftSwitches

class Memory:

  def __init__(self, num_banks=1, soft_switches=None):
    self.memory_banks = []
    self.current_bank = 0
    self.soft_switches = SoftSwitches() if soft_switches is not None else soft_switches
    for i in range(0, num_banks):
      self.memory_banks[i] = MemoryBank()

  def read(self, address):
    return self.memory_banks[self.current_bank].read(address)

  def write(self, address, value):
    self.memory_banks[self.current_bank].write(address, value)

  def switch_bank(self, bank_num):
    if len(self.memory_banks) < bank_num:
      raise Exception("Invalid bank number selected")
    self.current_bank = bank_num

