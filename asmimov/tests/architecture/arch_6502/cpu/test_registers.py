import unittest
from architecture.arch_6502.cpu.registers import Registers, \
  StackPointer, StatusRegister
from architecture.math.hexnum import ByteValue, WordValue

class RegistersTest(unittest.TestCase):

  # not doing much with these as i might change the general interface
  def test_registers_a(self):
    registers = Registers()
    registers.write("A", 0x78)
    a_reg = registers.read("A")
    self.assertIsInstance(a_reg, ByteValue)
    self.assertEqual(0x78, a_reg.value)

  def test_registers_x(self):
    registers = Registers()
    x_reg = registers.read("X")
    self.assertIsInstance(x_reg, ByteValue)
    x_reg.value = 0x8a
    registers.write("X", x_reg)
    self.assertEqual(0x8a, registers.read("X").value)

  def test_registers_y(self):
    registers = Registers()
    y_reg = registers.read("Y")
    self.assertIsInstance(y_reg, ByteValue)
    y_reg.value = 0x14
    registers.write("y", y_reg)
    self.assertEqual(0x14, registers.read("Y").value)

  def test_registers_sp(self):
    registers = Registers()
    sp_reg = registers.read("SP")
    self.assertIsInstance(sp_reg, StackPointer)
    sp_reg.value = 0xff
    registers.write("SP", sp_reg)
    self.assertEqual(0xff, registers.read("SP").value)

  def test_registers_p(self):
    registers = Registers()
    p_reg = registers.read("P")
    self.assertIsInstance(p_reg, StatusRegister)
    p_reg.value = 0xcf
    registers.write("P", p_reg)
    self.assertEqual(0xcf, registers.read("P").value)

  def test_registers_pc(self):
    registers = Registers()
    pc_reg = registers.read("PC")
    self.assertIsInstance(pc_reg, WordValue)
    pc_reg.value = 0x3f00
    registers.write("PC", pc_reg)
    self.assertEqual(0x3f00, registers.read("PC").value)
