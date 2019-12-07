import unittest
from architecture.arch_6502 import operations

class OperationsTest(unittest.TestCase):

  class Instruction:
    def __init__(self, tpl):
      self.tpl = tpl

    def metadata(self):
      return self.tpl


  def test_nop(self):
    result = operations.nop(None, None)
    self.assertEqual({}, result)

  def test_rol_no_carry_out_or_in(self):
    metadata = (0x01, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x02)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_rol_carry_in_not_out(self):
    metadata = (0x01, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x03)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_rol_negative_flag(self):
    metadata = (0x40, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x81)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)

  def test_rol_greater_than_128_rolls_correctly(self):
    metadata = (0x88, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x10)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_rol_greater_than_128_with_carry(self):
    metadata = (0x88, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x11)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)


if __name__ == "__main__":
  unittest.main()
