import unittest
from tests.architecture.arch_6502 import test_operations
from architecture.arch_6502 import operations

class OperationsShiftTest(test_operations.OperationsTest):
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

  def test_rol_carry_out_not_in(self):
    metadata = (0x84, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x08)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)


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

  def test_rol_results_in_zero(self):
    metadata = (0x80, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x00)
    self.assertEqual(dz, 1)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_rol_ff_handled_properly_no_carry(self):
    metadata = (0xff, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0xfe)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 1)

  def test_rol_ff_handled_properly_with_carry(self):
    metadata = (0xff, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.rol(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0xff)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 1)

  def test_ror_no_carry_in_or_out(self):
    metadata = (0x02, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.ror(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x01)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_ror_carry_in_not_out(self):
    metadata = (0x02, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.ror(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x81)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)

  def test_ror_carry_out_not_in(self):
    metadata = (0x11, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.ror(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x08)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_ror_negative_flag(self):
    metadata = (0x02, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.ror(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x81)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)

  def test_ror_results_in_negative_with_carry(self):
    metadata = (0x01, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.ror(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x80)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 1)

  def test_asl_no_carry_out(self):
    metadata = (0x01, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x02)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_asl_carry_out(self):
    metadata = (0x90, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x20)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_asl_carry_out_and_in(self):
    metadata = (0xa2, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x44)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)


  def test_rol_negative_flag(self):
    metadata = (0x44, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x88)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)

  def test_asl_results_in_zero(self):
    metadata = (0x80, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x00)
    self.assertEqual(dz, 1)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_asl_ff_handled_properly_no_carry(self):
    metadata = (0xff, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0xfe)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 1)

  def test_asl_ff_handled_properly_with_carry(self):
    metadata = (0xff, 1, "A")
    inst = self.Instruction(metadata)

    result = operations.asl(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0xfe)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 1)

  def test_lsr_no_carry_out_or_in(self):
    metadata = (0x10, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.lsr(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x08)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_lsr_carry_out(self):
    metadata = (0x0d, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.lsr(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x06)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_lsr_to_zero(self):
    metadata = (0x01, 0, "A")
    inst = self.Instruction(metadata)

    result = operations.lsr(None, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x00)
    self.assertEqual(dz, 1)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)


if __name__ == "__main__":
  unittest.main()
