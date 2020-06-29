import unittest
from tests.architecture.arch_6502.operations import test_operations
from architecture.arch_6502.cpu import cpu_container, operations

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
    system = cpu_container.CPUContainer(None, None, None, None, 0b11001100, 0xfe)

    result = operations.php(system, inst)
    sp_reg = result["SP"]
    self.assertEqual(sp_reg, 0xfd)
    stack_ptr_value = result[0x100 + sp_reg + 1]
    self.assertEqual(stack_ptr_value, 0b11111100)

  def test_plp(self):
    metadata = (0b11110011, None, "P")
    inst = self.Instruction(metadata)
    system = cpu_container.CPUContainer(None, None, None, None, None, 0xcf)
    self.assertEqual(system.cpu_register("P"), 0)

    result = operations.plp(system, inst)
    status = result["P"]
    self.assertEqual(status, 0b11000011)
    sp_reg = result["SP"]
    self.assertEqual(sp_reg, 0xd0)
    stack_ptr_value = result[0x100 + sp_reg - 1]
    self.assertEqual(stack_ptr_value, 0)

  def test_pha(self):
    metadata = (0x99, None, None)
    inst = self.Instruction(metadata)
    # getting close to a... (wait for it...)
    # STACK OVERFLOW
    # ...
    # ...
    # ... i'm here all week, folks!
    # also setting the actual A register in the oldcpu container is moot,
    # since the metadata already "got" it... but why not
    system = cpu_container.CPUContainer(0x99, None, None, None, None, 0x03)

    result = operations.pha(system, inst)
    sp_reg = result["SP"]
    self.assertEqual(sp_reg, 0x02)
    stack_ptr_value = result[sp_reg + 0x100 + 1]
    self.assertEqual(stack_ptr_value, 0x99)

  def test_pla(self):
    metadata = (0xfe, None, "A")
    inst = self.Instruction(metadata)
    system = cpu_container.CPUContainer(0x44, None, None, None, None, 0xb5)

    result = operations.pla(system, inst)
    a_reg = result["A"]
    self.assertEqual(a_reg, 0xfe)
    sp_reg = result["SP"]
    self.assertEqual(sp_reg, 0xb6)
    stack_ptr_value = result[0x100 + sp_reg - 1]
    self.assertEqual(stack_ptr_value, 0)

  def do_set_test(self, result, flag):
    self.do_setclear_test(result, flag, 1)

  def do_clear_test(self, result, flag):
    self.do_setclear_test(result, flag, 0)

  def do_setclear_test(self, result, flag, expect):
    self.assertIn("P", result)
    status = result["P"]
    self.assertIn(flag, status)
    self.assertEqual(status[flag], expect)
