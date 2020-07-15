import unittest

from architecture.math.hexnum import WordValue, ByteValue
from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

class CpuStatesReadTest(unittest.TestCase):

  def test_irq_vectors(self):
    cpu = CPU(Registers(), Memory())

    cpu.address_bus.set(0xfffc)
    cpu.address_bus.write(0x40)
    cpu.address_bus.set(0xfffd)
    cpu.address_bus.write(0x80)
    cpu.pc(0x8ffa)

    cpu, state = read_irq_vector_lo(cpu)
    self.assertEqual(0x40, cpu.pc().get_lo_byte().value)

    cpu, state = read_irq_vector_hi(cpu)
    self.assertEqual(0x80, cpu.pc().get_hi_byte().value)
    self.assertEqual(0x40, cpu.pc().get_lo_byte().value)
    self.assertEqual(0x8040, cpu.pc().get())

  def test_read_and_throw_away(self):
    cpu = CPU(Registers(), Memory())

    cpu.pc(0x7cff)

    cpu, state = read_next_and_throw_away(cpu)
    self.assertEqual(0x7cff, cpu.pc().get())

  def test_read_next_throw_away_inc_pc(self):
    cpu = CPU(Registers(), Memory())

    cpu.pc(0x7cff)

    cpu, state = read_next_throw_away_inc_pc(cpu)
    self.assertEqual(0x7d00, cpu.pc().get())

  def test_read_from_effective_address_with_without_pg_bnd_fix(self):
    cpu = CPU(Registers(), Memory())

    cpu.address_bus.set(0x70ff)
    cpu.address_bus.write(0x44)
    cpu.address_bus.set(0x7100)
    cpu.address_bus.write(0xcf)

    cpu.address_bus.set(0x70ff)
    cpu, state = read_from_effective_address(cpu)
    self.assertEqual(None, state)
    v = cpu.DR()
    self.assertEqual(0x44, v.value)

    cpu.pc(0x70ff)
    cpu.pc(cpu.pc() + 1)
    cpu.address_bus.set(cpu.pc())

    cpu, state = read_from_effective_fix_address(cpu)
    self.assertEqual(None, state)
    v = cpu.DR()
    self.assertEqual(0xcf, v.value)
    self.assertEqual(0x7100, cpu.address_bus.address_word.get())

