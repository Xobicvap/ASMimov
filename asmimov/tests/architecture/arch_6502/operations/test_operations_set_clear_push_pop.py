import unittest
from tests.architecture.arch_6502.operations import test_operations
from architecture.arch_6502.cpu import operations

class OperationsSetClearPushPopTest(test_operations.OperationsTest):
  
  def test_clc(self):
    self.do_clear_test(operations.clc(None, None), "C")

  def test_cli(self):
    self.do_clear_test(operations.cli(None, None), "I")

  def test_cld(self):
    self.do_clear_test(operations.cld(None, None), "D")

  def test_clv(self):
    self.do_clear_test(operations.clv(None, None), "V")

  def test_sec(self):
    self.do_set_test(operations.sec(None, None), "C")

  def test_sei(self):
    self.do_set_test(operations.sei(None, None), "I")

  def test_sed(self):
    self.do_set_test(operations.sed(None, None), "D")

  def test_php(self):
    metadata = (0b11001100, None, None)
    inst = self.Instruction(metadata)

    result = operations.php(None, inst)
    push_byte = result["push"]
    self.assertEqual(push_byte, 0b11111100)

  def test_plp(self):
    metadata = (0b11110011, None, "P")
    inst = self.Instruction(metadata)

    result = operations.plp(None, inst)
    status = result["P"]
    self.assertEqual(status, 0b11000011)
    pop_ct = result["pop"]
    self.assertEqual(pop_ct, 1)

  def test_pha(self):
    metadata = (0x99, None, None)
    inst = self.Instruction(metadata)

    result = operations.pha(None, inst)
    push_byte = result["push"]
    self.assertEqual(push_byte, 0x99)

  def test_pla(self):
    metadata = (0xfe, None, "A")
    inst = self.Instruction(metadata)

    result = operations.pla(None, inst)
    a_reg = result["A"]
    self.assertEqual(a_reg, 0xfe)
    pop_ct = result["pop"]
    self.assertEqual(pop_ct, 1)


  def do_set_test(self, result, flag):
    self.do_setclear_test(result, flag, 1)

  def do_clear_test(self, result, flag):
    self.do_setclear_test(result, flag, 0)

  def do_setclear_test(self, result, flag, expect):
    self.assertIn("P", result)
    status = result["P"]
    self.assertIn(flag, status)
    self.assertEqual(status[flag], expect)
