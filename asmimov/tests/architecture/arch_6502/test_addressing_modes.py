from architecture.arch_6502.cpu import addressing_modes
from architecture.arch_6502.cpu.cpu_container import CPUContainer
import unittest

class AddressingModesTest(unittest.TestCase):
  def test_pop_byte(self):
    system = CPUContainer(None, None, None, None, None, 0x6e,
                          {0x16f: 0xab})
    b = addressing_modes.pop_byte(system, "SP")
    self.assertEqual(b, 0xab)

  def test_pop_word(self):
    system = CPUContainer(None, None, None, None, None, 0x6e,
                          {0x16f: 0xab, 0x170: 0x80})
    lo, hi = addressing_modes.pop_word(system, "SP")
    self.assertEqual(lo, 0xab)
    self.assertEqual(hi, 0x80)

  def test_pop_addr(self):
    system = CPUContainer(None, None, None, None, None, 0x6e,
                          {0x16f: 0xab, 0x170: 0x80})
    addr = addressing_modes.pop_addr(system, "SP")
    self.assertEqual(addr, 0x80ab)

  def test_indirect_simple(self):
    system = CPUContainer(None, None, None, 0x7000, None, None,
                          {0x8000: 0x10, 0x8001: 0x20})
    addr, _ = addressing_modes.indirect(system, 0x8000, None)
    self.assertEqual(addr, 0x2010)

  def test_indirect_with_last_byte_bug(self):
    system = CPUContainer(None, None, None, 0x7000, None, None,
                          {0x8000: 0x10, 0x8001: 0x20, 0x80ff: 0x20,
                           0x8100: 0x80})
    addr, _ = addressing_modes.indirect(system, 0x80ff, None)
    self.assertEqual(addr, 0x1020)

  def test_indexed_indirect(self):
    system = CPUContainer(None, 0xf, None, 0x7000, None, None,
                          {0x53: 0x80, 0x54: 0x02, 0x55: 0x9e,
                           0x0280: 0xf2, 0x9e02: 0x8f})
    result, cycles = addressing_modes.indexed_indirect(system, 0x45, 6)
    self.assertEqual(result, 0x8f)
    self.assertEqual(cycles, 6)

  def test_indexed_indirect_page_boundary_not_counted(self):
    system = CPUContainer(None, 0xad, None, 0x7000, None, None,
                          {0x22: 0x3b, 0x23: 0xfe, 0x122: 0x24,
                           0x123: 0xd4, 0xfe3b: 0x06})
    result, cycles = addressing_modes.indexed_indirect(system, 0x75, 6)
    self.assertEqual(result, 0x06)
    self.assertEqual(cycles, 6)

  def test_indirect_indexed_simple(self):
    system = CPUContainer(None, None, 0x10, 0x7000, None, None,
                          {0x86: 0x28, 0x87: 0x40, 0x96: 0xdf,
                           0x97: 0x53, 0x4038: 0xb5, 0x53df: 0xff})
    result, cycles = addressing_modes.indirect_indexed(system, 0x86, 5)
    self.assertEqual(result, 0xb5)
    self.assertEqual(cycles, 5)

  def test_indirect_indexed_page_boundary_crossed(self):
    system = CPUContainer(None, None, 0xf8, 0x7000, None, None,
                          {0xf0: 0x80, 0xf1: 0x40, 0xf2: 0xdf,
                           0x4078: 0x83, 0x4178: 0x21})
    result, cycles = addressing_modes.indirect_indexed(system, 0xf0, 5)
    self.assertEqual(result, 0x83)
    self.assertEqual(cycles, 6)

  def test_zero_page(self):
    system = CPUContainer(None, None, None, 0x7000, None, None,
                          {0x60: 0x80, 0x61: 0x02})
    result, _ = addressing_modes.zero_page(system, 0x60, None)
    self.assertEqual(result, 0x80)

  def test_absolute(self):
    system = CPUContainer(None, None, None, 0x7000, None, None,
                          {0x8000: 0x10, 0x8001: 0x20})
    result, _ = addressing_modes.absolute(system, 0x8001, None)
    self.assertEqual(result, 0x20)

  def test_absolute_x_simple(self):
    system = CPUContainer(None, 0x57, None, 0x7000, None, None,
                          {0x5023: 0x10, 0x5057: 0x20, 0x507a: 0x96})
    result, cycles = addressing_modes.absolute_x(system, 0x5023, 4)
    self.assertEqual(result, 0x96)
    self.assertEqual(cycles, 4)

  def test_absolute_x_page_boundary(self):
    system = CPUContainer(None, 0x76, None, 0x7000, None, None,
                          {0xcabc: 0x55, 0xca32: 0x78, 0xcb32: 0x99})
    result, cycles = addressing_modes.absolute_x(system, 0xcabc, 4)
    self.assertEqual(result, 0x78)
    self.assertEqual(cycles, 5)

  def test_absolute_y_simple(self):
    system = CPUContainer(None, None, 0x24, 0x7000, None, None,
                          {0x07db: 0xab, 0x700: 0x05, 0x7ff: 0x12})
    result, cycles = addressing_modes.absolute_y(system, 0x07db, 4)
    self.assertEqual(result, 0x12)
    self.assertEqual(cycles, 4)

  def test_absolute_y_page_boundary(self):
    system = CPUContainer(None, None, 0x86, 0x7000, None, None,
                          {0xe1ed: 0x15, 0xe173: 0x45, 0xe273: 0x4d})
    result, cycles = addressing_modes.absolute_y(system, 0xe1ed, 4)
    self.assertEqual(result, 0x45)
    self.assertEqual(cycles, 5)

  def test_zero_page_x_simple(self):
    system = CPUContainer(None, 0xb8, None, 0x7000, None, None,
                          {0x39: 0x34, 0xf1: 0xeb, 0xf2: 0x0d})
    result, cycles = addressing_modes.zero_page_x(system, 0x39, 3)
    self.assertEqual(result, 0xeb)
    self.assertEqual(cycles, 3)

  def test_zero_page_x_page_boundary(self):
    system = CPUContainer(None, 0x67, None, 0x7000, None, None,
                          {0xc4: 0x03, 0x12b: 0xd4, 0x2b: 0xcb})
    result, cycles = addressing_modes.zero_page_x(system, 0xc4, 3)
    self.assertEqual(result, 0xcb)
    self.assertEqual(cycles, 4)

  def test_zero_page_y_simple(self):
    system = CPUContainer(None, None, 0xa3, 0x7000, None, None,
                          {0x21: 0x34, 0xc4: 0xb4, 0xc5: 0x9b})
    result, cycles = addressing_modes.zero_page_y(system, 0x21, 3)
    self.assertEqual(result, 0xb4)
    self.assertEqual(cycles, 3)

  def test_zero_page_y_page_boundary(self):
    system = CPUContainer(None, None, 0x09, 0x7000, None, None,
                          {0xf7: 0xd1, 0x100: 0xa5, 0x00: 0x8e})
    result, cycles = addressing_modes.zero_page_y(system, 0xf7, 3)
    self.assertEqual(result, 0x8e)
    self.assertEqual(cycles, 4)
