import unittest
from random import randrange
from architecture.arch_6502.cpu.cpu_container import CPUContainer

class CPUContainerTest(unittest.TestCase):

  def test_status_get_whole_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b10000001)

    status = cpu.status()
    self.assertEqual(0b10000001, status)

  def test_status_get_n_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b10000001)

    status = cpu.status("N")
    self.assertEqual(1, status)

    cpu = CPUContainer(None, None, None, None, 0b00000000)
    status = cpu.status("N")
    self.assertEqual(0, status)

  def test_status_get_v_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b11000001)

    status = cpu.status("V")
    self.assertEqual(1, status)

    cpu = CPUContainer(None, None, None, None, 0b00000000)
    status = cpu.status("V")
    self.assertEqual(0, status)

  def test_status_get_d_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b00001001)

    status = cpu.status("D")
    self.assertEqual(1, status)

    cpu = CPUContainer(None, None, None, None, 0b00000000)
    status = cpu.status("D")
    self.assertEqual(0, status)

  def test_status_get_i_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b00000101)

    status = cpu.status("I")
    self.assertEqual(1, status)

    cpu = CPUContainer(None, None, None, None, 0b00000000)
    status = cpu.status("I")
    self.assertEqual(0, status)

  def test_status_get_z_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b00000011)

    status = cpu.status("Z")
    self.assertEqual(1, status)

    cpu = CPUContainer(None, None, None, None, 0b00000000)
    status = cpu.status("Z")
    self.assertEqual(0, status)

  def test_status_get_c_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b00000001)

    status = cpu.status("C")
    self.assertEqual(1, status)

    cpu = CPUContainer(None, None, None, None, 0b00000000)
    status = cpu.status("C")
    self.assertEqual(0, status)

  def test_status_get_unknown_flag(self):
    cpu = CPUContainer(None, None, None, None, 0b00000001)
    self.assertRaises(Exception, cpu.status, "J")

  def test_status_write_n_simple(self):
    self.status_write_flag_simple_test("N", 0b10000000)

  def test_status_write_n_other_bits_preserved(self):
    self.status_write_flag_other_bits_preserved("N", 0b11001001, 0b01001001)

  def test_status_write_v_simple(self):
    self.status_write_flag_simple_test("V", 0b01000000)

  def test_status_write_v_other_bits_preserved(self):
    self.status_write_flag_other_bits_preserved("V", 0b11001001, 0b10001001)

  def test_status_write_d_simple(self):
    self.status_write_flag_simple_test("D", 0b00001000)

  def test_status_write_d_other_bits_preserved(self):
    self.status_write_flag_other_bits_preserved("D", 0b11001001, 0b11000001)

  def test_status_write_i_simple(self):
    self.status_write_flag_simple_test("I", 0b00000100)

  def test_status_write_i_other_bits_preserved(self):
    self.status_write_flag_other_bits_preserved("I", 0b11001101, 0b11001001)

  def test_status_write_z_simple(self):
    self.status_write_flag_simple_test("Z", 0b00000010)

  def test_status_write_z_other_bits_preserved(self):
    self.status_write_flag_other_bits_preserved("Z", 0b11001011, 0b11001001)

  def test_status_write_c_simple(self):
    self.status_write_flag_simple_test("C", 0b00000001)

  def test_status_write_c_other_bits_preserved(self):
    self.status_write_flag_other_bits_preserved("C", 0b11001001, 0b11001000)

  def test_cpu_registers(self):
    cpu = CPUContainer()
    regs = cpu.cpu_registers()
    self.assertIn("A", regs)
    self.assertIn("X", regs)
    self.assertIn("Y", regs)
    self.assertIn("PC", regs)
    self.assertIn("P", regs)
    self.assertIn("SP", regs)

  def test_a_register_read_write_read(self):
    self.cpu_register_read_write_read_test("A", 0x7f, 0x90)
    self.cpu_register_read_write_read_test("A", randrange(0, 0x100), randrange(0, 0x100))

  def test_x_register_read_write_read(self):
    self.cpu_register_read_write_read_test("X", 0x7f, 0x90)
    self.cpu_register_read_write_read_test("X", randrange(0, 0x100), randrange(0, 0x100))

  def test_y_register_read_write_read(self):
    self.cpu_register_read_write_read_test("Y", 0x7f, 0x90)
    self.cpu_register_read_write_read_test("Y", randrange(0, 0x100), randrange(0, 0x100))

  def test_pc_register_read_write_read(self):
    self.cpu_register_read_write_read_test("PC", 0x7f00, 0x9000)
    self.cpu_register_read_write_read_test("PC", randrange(0, 0x10000), randrange(0, 0x10000))

  def test_p_register_read_write_read(self):
    self.cpu_register_read_write_read_test("P", 0x7f, 0x90)
    self.cpu_register_read_write_read_test("P", randrange(0, 0x100), randrange(0, 0x100))

  def test_sp_register_read_write_read(self):
    self.cpu_register_read_write_read_test("SP", 0x7f, 0x90)
    self.cpu_register_read_write_read_test("SP", randrange(0, 0x100), randrange(0, 0x100))

  def test_read_for_a_register(self):
    cpu = CPUContainer(0x88, 0x74)
    self.read_test_for_registers(cpu, "A", 0x88)

  def test_read_for_x_register(self):
    cpu = CPUContainer(0x88, 0x74)
    self.read_test_for_registers(cpu, "X", 0x74)

  def test_read_for_y_register(self):
    cpu = CPUContainer(0x88, 0x74, 0x12)
    self.read_test_for_registers(cpu, "Y", 0x12)

  def test_read_for_pc_register(self):
    cpu = CPUContainer(0x88, 0x74, 0x12, 0x8400)
    self.read_test_for_registers(cpu, "PC", 0x8400)

  def test_read_for_p_register(self):
    cpu = CPUContainer(0x88, 0x74, 0x12, 0x8400, 0x89)
    self.read_test_for_registers(cpu, "P", 0x89)

  def test_read_for_sp_register(self):
    cpu = CPUContainer(0x88, 0x74, 0x12, 0x8400, 0x89, 0xf2)
    self.read_test_for_registers(cpu, "SP", 0xf2)

  # do read test with addr fxns AFTER we do addressing mode tests

  def test_read_direct(self):
    cpu = CPUContainer(None, None, None, None, None, None, {0x1000: 0x7f, 0x1001: 0x92, 0x8000: 0x10})
    v = cpu.read_direct(0x1000)
    self.assertEqual(v, 0x7f)

    v = cpu.read_direct(0x1001)
    self.assertEqual(v, 0x92)

    v = cpu.read_direct(0x8000)
    self.assertEqual(v, 0x10)

  def test_read_absolute_address(self):
    cpu = CPUContainer(None, None, None, None, None, None, {0x1000: 0x7f, 0x1001: 0x92, 0x8000: 0x10})
    addr = cpu.read_absolute_address(0x1000)
    self.assertEqual(addr, 0x927f)

  def test_write_memory_then_read(self):
    cpu = CPUContainer()
    cpu.write(0x700, 0xff)
    v = cpu.read_direct(0x700)
    self.assertEqual(v, 0xff)

  def test_vector_address(self):
    memory_map = {0xfffa: 0x14, 0xfffb: 0x80, 0xfffc: 0, 0xfffd: 0x80, 0xfffe: 0x80, 0xffff: 0x90}
    cpu = CPUContainer(None, None, None, None, None, None, memory_map)
    addr = cpu.vector("IRQ/BRK")
    self.assertEqual(addr, 0x9080)

    addr = cpu.vector("RESET")
    self.assertEqual(addr, 0x8000)

    addr = cpu.vector("NMI")
    self.assertEqual(addr, 0x8014)

  def test_change(self):
    # this covers just about the entire change set in one test
    cpu = CPUContainer()
    change_map = {
      "A": 0x9f,
      "P": {"N": 1, "V": 1, "Z": 0}
    }
    cpu.change(**change_map)
    a_reg = cpu.cpu_register("A")
    self.assertEqual(a_reg, 0x9f)

    status = cpu.cpu_register("P")
    self.assertEqual(status, 0b11000000)

    change_map = {
      "X": 0x23
    }

  def status_write_flag_simple_test(self, flag, expect):
    cpu = CPUContainer()
    status_reg = {flag: 1}
    cpu.status_write(status_reg)
    status = cpu.status()
    self.assertEqual(expect, status)

  def status_write_flag_other_bits_preserved(self, flag, expect_on, expect_off):
    cpu = CPUContainer(None, None, None, None, expect_off)
    status_reg = {flag: 1}
    cpu.status_write(status_reg)
    status = cpu.status()
    self.assertEqual(expect_on, status)

    status_reg[flag] = 0
    cpu.status_write(status_reg)
    status = cpu.status()
    self.assertEqual(expect_off, status)

  def cpu_register_read_write_read_test(self, reg, reg_val_r, reg_val_write):
    # we're cheating with this test and setting EVERY register to
    # reg_val_r initially, but only writing / reading the specified register
    cpu = CPUContainer(reg_val_r, reg_val_r, reg_val_r, reg_val_r, reg_val_r, reg_val_r)
    read1 = cpu.cpu_register(reg)
    self.assertEqual(reg_val_r, read1)
    cpu.cpu_register(reg, reg_val_write)
    read2 = cpu.cpu_register(reg)
    self.assertEqual(reg_val_write, read2)

  def read_test_for_registers(self, cpu, reg, exp_reg_val):
    val = cpu.read(reg)
    self.assertEqual(exp_reg_val, val)






