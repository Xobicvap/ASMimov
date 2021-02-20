import unittest

from architecture.arch_6502.system.system_cpu import SystemCPU
from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_cycle_fxns import *

class SystemCpuAggregationTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory(), True)

  def test_brk_php_aggregation_end(self):
    cpu = self.cpu

    cpu.sp(0xff)
    cpu.p(0b10000101)
    cpu.pc(0x8001)

    cpu.address_bus.memset({
      0x8001: 0x00,
      0x8002: 0x78,
      0x8102: 0x08,
      0xfffe: 0x02,
      0xffff: 0x81
    })

    sys = SystemCPU(cpu, True)
    sys.step()
    while len(sys.current_steps) > 0:
      sys.step()
    sys.step()
    while len(sys.current_steps) > 0:
      sys.step()
    print(sys.aggregator)
