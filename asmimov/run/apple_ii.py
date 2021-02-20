from architecture.arch_6502.cpu import *
from architecture.arch_6502.system import *

class AppleII:

  def __init__(self):
    registers = Registers()
    memory = Memory()
    self.cpu = CPU(registers, memory)

  def register_systems(self, ):
