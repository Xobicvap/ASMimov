import unittest
from tests.architecture.arch_6502 import test_operations
from architecture.arch_6502 import operations

class OperationsArithmeticTest(test_operations.OperationsTest):

  def test_adc_simple(self):
    metadata = (0x01, 0x01, "A")
    sys = self.TestSystem({"C": 0, "D": 0})

    inst = self.Instruction(metadata)

    result = operations.adc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x02)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_adc_with_carry_simple(self):
    """
    You wouldn't normally do ADC without CLC first, but 
    it doesn't mean you _can't_!
    """
    metadata = (0x01, 0x01, "A")
    sys = self.TestSystem({"C": 1, "D": 0})

    inst = self.Instruction(metadata)

    result = operations.adc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x03)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_adc_with_decimal_simple(self):
    metadata = (0x05, 0x05, "A")
    sys = self.TestSystem({"C": 0, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.adc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x10)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 0)

  def test_adc_with_decimal_carry_out(self):
    metadata = (0x58, 0x46, "A")
    sys = self.TestSystem({"C": 0, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.adc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x04)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_adc_with_decimal_carry_acc_zero_but_zero_flag_off(self):
    """
    This is one of those "undocumented" 6502 features, so you know
    this emulates the 6502 properly. If an operation results in 0
    but the carry flag is set, the Z flag will be 0! On the 65C02
    apparently this does NOT happen.
    """
    metadata = (0x81, 0x19, "A")
    sys = self.TestSystem({"C": 0, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.adc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x00)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_adc_decimal_negative_flag_set_according_to_accumulator(self):
    """
    The N flag in decimal mode is weird but it's supposed to match the
    accumulator...
    """

    metadata = (0x75, 0x10, "A")
    sys = self.TestSystem({"C": 0, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.adc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x85)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)


  def test_sbc_simple(self):
    metadata = (0x02, 0x01, "A")
    # for simple cases like this we'll assume the programmer did the
    # correct thing and _set_ the carry as you should before SBC
    sys = self.TestSystem({"C": 1, "D": 0})
    inst = self.Instruction(metadata)

    result = operations.sbc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x01)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_sbc_no_carry_simple(self):
    metadata = (0x03, 0x01, "A")
    sys = self.TestSystem({"C": 0, "D": 0})
    inst = self.Instruction(metadata)

    result = operations.sbc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x01)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_sbc_decimal_simple(self):
    metadata = (0x65, 0x23, "A")
    sys = self.TestSystem({"C": 1, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.sbc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x42)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_sbc_decimal_with_borrow(self):
    metadata = (0x81, 0x68, "A")
    sys = self.TestSystem({"C": 1, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.sbc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x13)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_sbc_decimal_no_carry_out_negative(self):
    metadata = (0x42, 0x62, "A")
    sys = self.TestSystem({"C": 1, "D": 1})
    inst = self.Instruction(metadata)

    result = operations.sbc(sys, inst)
    dv = result["A"]
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dv, 0x80)
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)


  def test_cmp_result_negative(self):
    metadata = (0x23, 0x50, '')
    inst = self.Instruction(metadata)

    result = operations.cmp8(None, inst)
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 0)

  def test_cmp_result_positive_with_carry(self):
    metadata = (0x50, 0x23, '')
    inst = self.Instruction(metadata)

    result = operations.cmp8(None, inst)
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_cmp_result_two_negatives_in_positive_with_carry_out(self):
    metadata = (0xf0, 0xe0, '')
    inst = self.Instruction(metadata)

    result = operations.cmp8(None, inst)
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  def test_cmp_result_negative_with_carry(self):
    metadata = (0xf0, 0x70, '')
    inst = self.Instruction(metadata)

    result = operations.cmp8(None, inst)
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dz, 0)
    self.assertEqual(dn, 1)
    self.assertEqual(dc, 1)

  def test_cmp_result_zero_with_carry(self):
    metadata = (0xf0, 0xf0, '')
    inst = self.Instruction(metadata)

    result = operations.cmp8(None, inst)
    dp = result["P"]
    dz = dp["Z"]
    dn = dp["N"]
    dc = dp["C"]
    self.assertEqual(dz, 1)
    self.assertEqual(dn, 0)
    self.assertEqual(dc, 1)

  # since CPX / CPY go through the same compare() function, and we're
  # specifying the value as l as it is... these tests are skipped


