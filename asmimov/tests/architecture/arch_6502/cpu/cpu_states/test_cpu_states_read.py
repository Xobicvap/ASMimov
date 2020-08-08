import unittest

from architecture.math.hexnum import WordValue, ByteValue
from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

class CpuStatesReadTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory())

  def test_irq_vectors(self):
    self.cpu.address_set(0xfffe)
    self.cpu.address_bus.write(0x40)
    self.cpu.address_set(0xffff)
    self.cpu.address_bus.write(0x80)
    self.cpu.pc(0x8ffa)

    self.cpu, state = read_irq_vector_lo(self.cpu)
    self.assertEqual(0x40, self.cpu.pc().get_lo_byte().value)

    self.cpu, state = read_irq_vector_hi(self.cpu)
    self.assertEqual(0x80, self.cpu.pc().get_hi_byte().value)
    self.assertEqual(0x40, self.cpu.pc().get_lo_byte().value)
    self.assertEqual(0x8040, self.cpu.pc().get())

  def test_read_and_throw_away(self):
    self.cpu.pc(0x7cff)

    self.cpu, state = read_next_and_throw_away(self.cpu)
    self.assertEqual(0x7cff, self.cpu.pc().get())

  def test_read_next_throw_away_inc_pc(self):
    self.cpu.pc(0x7cff)

    self.cpu, state = read_next_throw_away_inc_pc(self.cpu)
    self.assertEqual(0x7d00, self.cpu.pc().get())

  def test_read_from_effective_address_with_without_pg_bnd_fix(self):
    self.cpu.address_set(0x70ff)
    self.cpu.address_bus.write(0x44)
    self.cpu.address_set(0x7100)
    self.cpu.address_bus.write(0xcf)

    self.cpu.address_set(0x70ff)
    self.cpu, state = read_from_effective_address(self.cpu)
    self.assertEqual(None, state)
    v = self.cpu.DR()
    self.assertEqual(0x44, v.value)

    self.cpu.pc(0x70ff)
    self.cpu.pc(self.cpu.pc() + 1)
    self.cpu.address_set(self.cpu.pc())

    self.cpu, state = read_from_effective_fix_address(self.cpu)
    self.assertEqual(None, state)
    v = self.cpu.DR()
    self.assertEqual(0xcf, v.value)
    self.assertEqual(0x7100, self.cpu.address_bus.address_word.get())

  def test_read_effective_add_index(self):
    self.cpu.address_set(0xfbcd)
    self.cpu.address_bus.write(0x88)
    self.cpu.address_set(0xfb01)
    self.cpu.address_bus.write(0xee)

    self.cpu.y(0xcc)
    self.cpu, state = read_effective_add_y(self.cpu)

    address_read_from = self.cpu.address_bus.address_word.get()
    self.assertEqual(0xfbcd, address_read_from)
    self.assertEqual(None, state)

    self.cpu.x(0x34)
    self.cpu, state = read_effective_add_x(self.cpu)
    address_read_from = self.cpu.address_bus.address_word.get()
    self.assertEqual(0xfb01, address_read_from)
    self.assertEqual(None, state)

  def test_read_pointer_add_x(self):
    self.cpu.DR(0x62)
    self.cpu.x(0x13)

    self.cpu, state = read_pointer_add_x(self.cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x75, self.cpu.DR().value)





