import unittest

from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

class CpuStatesFetchTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory())

  def test_copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch(self):
    cpu = self.cpu
    cpu.address_bus.set(0xe002)
    cpu.address_bus.write(0x80)

    # in real life the preceding cycles would have advanced the PC to this,
    # if the JMP/JSR started at e000
    cpu.pc(0xe002)
    cpu.DR(0xa0)

    cpu, state = copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0x80a0, cpu.pc().value)

  def test_fetch_instruction(self):
    cpu = self.cpu
    cpu.address_bus.set(0x9000)
    cpu.address_bus.write(0x4d)

    cpu.pc(0x9000)
    cpu, state = fetch_instruction(cpu)
    self.assertEqual(False, state)
    self.assertEqual(0x9001, cpu.pc().value)
    self.assertEqual(0x4d, cpu.IR().value)

  def test_fetch_value_and_increment_pc(self):
    cpu = self.cpu
    cpu.address_bus.set(0xbf30)
    cpu.address_bus.write(0x02)

    cpu.pc(0xbf30)
    cpu, state = fetch_value_and_increment_pc(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0xbf31, cpu.pc().value)
    self.assertEqual(0x02, cpu.DR().value)

  def test_fetch_address_increment_pc(self):
    cpu = self.cpu
    cpu.address_bus.set(0xd6f2)
    cpu.address_bus.write(0x94)

    cpu.pc(0xd6f2)
    cpu, state = fetch_address_lo_byte_increment_pc(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0xd6f3, cpu.pc().value)
    self.assertEqual(0x94, cpu.DR().value)

    cpu.address_bus.set(cpu.pc())
    cpu.address_bus.write(0xff)

    cpu, state = fetch_address_hi_byte_increment_pc(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0xd6f4, cpu.pc().value)
    self.assertEqual(0xff94, cpu.address_bus.address_word.get())

  def test_fetch_pch_copy_to_pc(self):
    cpu = self.cpu
    cpu.DR(0x14)

    cpu.address_bus.memset({
      0xc601: 0x14,
      0xc602: 0x83
    })

    cpu.address_bus.set(0xc601)
    cpu.pc(0xc601)

    cpu, state = fetch_pch_copy_to_pc(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0x8314, cpu.pc().value)

    cpu.address_bus.memset({
      0xaaff: 0x03,
      0xaa00: 0xf2
    })

    cpu.DR(0x03)

    cpu.address_bus.set(0xaaff)
    cpu.pc(0xaaff)

    cpu, state = fetch_pch_copy_to_pc(cpu)
    self.assertEqual(True, state)
    self.assertEqual(0xf203, cpu.pc().value)

  def test_fetch_address_hi_byte_add_index_lo_increment_pc(self):
    cpu = self.cpu
    cpu.DR(0x70)
    cpu.pc(0xd602)

    cpu.address_bus.memset({
      0xd602: 0x85
    })
    cpu.x(0x11)
    cpu, state = fetch_address_hi_byte_add_x_lo_increment_pc(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x8581, cpu.address_bus.address_word.value)

    cpu.DR(0xf7)
    cpu.pc(0x8ffe)

    cpu.address_bus.memset({
      0x8ffe: 0x92
    })
    cpu.y(0x0a)
    cpu, state = fetch_address_hi_byte_add_y_lo_increment_pc(cpu)
    self.assertEqual(None, state)
    # this doesn't correct high byte at this step so this should not be 0x9301
    self.assertEqual(0x9201, cpu.address_bus.address_word.value)

  def test_fetch_address_zero_page_increment_pc(self):
    cpu = self.cpu
    cpu.pc(0xca76)

    cpu.address_bus.memset({
      0xca76: 0x30
    })

    cpu, state = fetch_address_zero_page_increment_pc(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x0030, cpu.address_bus.address_word.value)

  def test_fetch_indirect_effective_address_lo_and_hi_plus_y(self):
    cpu = self.cpu
    cpu.DR(0xa0)
    cpu.address_bus.memset({
      0x0a0: 0x44,
      0x0a1: 0x05
    })
    cpu.y(0xf6)

    cpu, state = fetch_indirect_effective_address_lo(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0x44, cpu.D2().value)

    cpu, state = fetch_indirect_effective_address_hi_add_y(cpu)
    self.assertEqual(0x05, cpu.DR().value)
    self.assertEqual(0x3a, cpu.D2().value)
    self.assertTrue(cpu.fix_effective)
    self.assertEqual(None, state)





