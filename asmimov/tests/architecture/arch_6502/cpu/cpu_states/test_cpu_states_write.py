from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

import unittest

class CpuStatesWriteTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory())

  def test_write_byte_to_effective_address(self):
    cpu = self.cpu

    cpu.DR(0x22)
    cpu.address_set(0x8702)
    cpu, state = write_back_to_effective_address(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x22, cpu.address_read().value)

    cpu.address_set(0x8756)
    cpu, state = write_new_to_effective_address(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0x22, cpu.address_read().value)

  def test_write_registers_to_effective_address(self):
    cpu = self.cpu

    cpu.a(0x78)
    cpu.x(0xfd)
    cpu.y(0x01)

    cpu.address_set(0x45)
    cpu, state = write_a_to_effective_address(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0x78, cpu.address_read().value)

    cpu.address_set(0x242)
    cpu, state = write_x_to_effective_address(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0xfd, cpu.address_read().value)

    cpu.address_set(0x378)
    cpu, state = write_y_to_effective_address(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0x01, cpu.address_read().value)

