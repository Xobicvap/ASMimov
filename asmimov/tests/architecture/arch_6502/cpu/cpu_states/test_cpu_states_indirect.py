from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

import unittest

class CpuStatesIndirectTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory())

  def test_indexed_indirect_address_lo(self):
    cpu = self.cpu

    cpu.DR(0x5b)
    cpu.address_bus.memset({
      0x05b: 0x9d
    })

    cpu, state = indexed_indirect_address_lo(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x9d, cpu.D2().value)

  def test_indexed_indirect_address_hi(self):
    cpu = self.cpu

    cpu.DR(0x4e)
    cpu.D2(0x02)

    cpu.address_bus.memset({
      0x004e: 0x04,
      0x004f: 0x07
    })

    cpu, state = indexed_indirect_address_hi(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x0702, cpu.address_bus.address_word.value)

  def test_indirect_indexed_read_and_fix(self):
    # first test shouldn't fix address
    cpu = self.cpu

    cpu.DR(0x06)
    cpu.D2(0x88)
    cpu.address_bus.memset({
      0x688: 0x0c,
      0x788: 0x5e
    })

    cpu, state = indirect_indexed_read_and_fix(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0x0c, cpu.DR().value)
    self.assertEqual(0x0688, cpu.address_bus.address_word.value)

    cpu.fix_effective = True
    cpu, state = indirect_indexed_read_and_fix(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x0d, cpu.DR().value)
    self.assertEqual(0x0c88, cpu.address_bus.address_word.value)
