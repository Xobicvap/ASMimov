import unittest

from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.cpu_states import *

class CpuStatesTest(unittest.TestCase):

  def test_increment_pc_no_new_page(self):

    cpu = CPU(Registers(), None)
    cpu.pc(0xf000)

    cpu = increment_pc(cpu)
    self.assertEqual(0xf001, cpu.pc().get())

  def test_increment_pc_new_page(self):
    cpu = CPU(Registers(), None)
    cpu.pc(0xe1ff)

    cpu = increment_pc(cpu)
    self.assertEqual(0xe200, cpu.pc().get())

