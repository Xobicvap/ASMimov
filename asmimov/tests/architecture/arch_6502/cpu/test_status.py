import unittest
from architecture.arch_6502.cpu.status import StatusRegister

class StatusRegisterTest(unittest.TestCase):

  def test_init_and_get_flags(self):
    # N flag, V flag, no D or I, Z flag, no C
    v = StatusRegister(0xc2)
    # make sure flag name is coerced to upper
    self.assertEqual(1, v.get_flag("n"))
    self.assertEqual(1, v.get_flag("V"))
    self.assertEqual(0, v.get_flag("D"))
    self.assertEqual(0, v.get_flag("I"))
    self.assertEqual(1, v.get_flag("z"))
    self.assertEqual(0, v.get_flag("C"))

    v = StatusRegister(0x0d)
    self.assertEqual(0, v.get_flag("N"))
    self.assertEqual(0, v.get_flag("V"))
    self.assertEqual(1, v.get_flag("d"))
    self.assertEqual(1, v.get_flag("I"))
    self.assertEqual(0, v.get_flag("z"))
    self.assertEqual(1, v.get_flag("c"))

  def test_set_flags(self):
    v = StatusRegister(0b10000010)
    self.assertEqual(1, v.get_flag("N"))
    self.assertEqual(0, v.get_flag("V"))
    self.assertEqual(0, v.get_flag("D"))
    self.assertEqual(0, v.get_flag("I"))
    self.assertEqual(1, v.get_flag("Z"))
    self.assertEqual(0, v.get_flag("C"))
    v.set_flags(0b11000110)
    self.assertEqual(1, v.get_flag("N"))
    self.assertEqual(1, v.get_flag("V"))
    self.assertEqual(0, v.get_flag("D"))
    self.assertEqual(1, v.get_flag("I"))
    self.assertEqual(1, v.get_flag("Z"))
    self.assertEqual(0, v.get_flag("C"))

  def test_set_flags_with_bit_name(self):
    v = StatusRegister(0x02)
    v.set_flags(0, "Z")
    self.assertEqual(0, v.get_flag("Z"))
    v.set_flags(1, "C")
    self.assertEqual(1, v.get_flag("C"))

  def test_modify_get_flag(self):
    v = StatusRegister(0x01)
    x = v.modify("C")
    self.assertEqual(1, x)

  def test_modify_set_flag(self):
    v = StatusRegister(0x41)
    v.modify("C", 0)
    v.modify("N", 1)
    self.assertEqual(1, v.get_flag("N"))
    self.assertEqual(0, v.get_flag("C"))
    # ensure other already-set flags are not affected
    self.assertEqual(1, v.get_flag("V"))
