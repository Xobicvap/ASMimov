from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu import CPU

from architecture.arch_6502.system.system_cpu import SystemCPU

class AppleII:

  def register_systems(self, config):
    registers = Registers()
    memory = Memory()
    cpu = CPU(registers, memory, config.aggregate)
    sys_cpu = SystemCPU(cpu, config.aggregate)
    # should check for other systems eventually
    return [sys_cpu]

