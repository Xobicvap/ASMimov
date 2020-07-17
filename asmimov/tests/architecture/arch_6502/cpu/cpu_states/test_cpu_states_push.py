import unittest

from architecture.math.hexnum import WordValue, ByteValue
from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

class CpuStatesPushPullTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory())

  def test_increment_pc_no_new_page(self):
    self.cpu.pc(0xf000)

    self.cpu = increment_pc(self.cpu)
    self.assertEqual(0xf001, self.cpu.pc().get())

  def test_increment_pc_new_page(self):
    self.cpu.pc(0xe1ff)

    self.cpu = increment_pc(self.cpu)
    self.assertEqual(0xe200, self.cpu.pc().get())

  def test_increment_sp_no_wrap(self):
    self.cpu.sp(0xfd)

    self.cpu, state = increment_sp(self.cpu)
    self.assertEqual(0xfe, self.cpu.sp().value)
    self.assertEqual(None, state)

  def test_increment_sp_wrap(self):
    self.cpu.sp(0xff)

    self.cpu, state = increment_sp(self.cpu)
    self.assertEqual(0x00, self.cpu.sp().value)
    self.assertEqual(None, state)

  def test_decrement_sp_no_wrap(self):
    self.cpu.sp(0xff)

    self.cpu, state = decrement_sp(self.cpu)
    self.assertEqual(0xfe, self.cpu.sp().value)
    self.assertEqual(None, state)

  def test_decrement_sp_wrap(self):
    self.cpu.sp(0x00)

    self.cpu, state = decrement_sp(self.cpu)
    self.assertEqual(0xff, self.cpu.sp().value)
    self.assertEqual(None, state)

  def test_address_of_stack(self):
    self.cpu.sp(0xff)

    self.cpu = address_of_stack(self.cpu)
    address = self.cpu.address_bus.address_word

    self.assertEqual(0x01ff, address.get())

  def test_push_pc_and_decrement_sp(self):
    self.cpu.sp(0xfc)
    self.cpu.pc(WordValue(0x6002))

    self.cpu, state = push_pch_and_decrement_sp(self.cpu)
    self.assertEqual(0x01fc, self.cpu.address_bus.address_word.get())
    self.assertEqual(0xfb, self.cpu.sp().value)
    pushed_value = self.cpu.address_bus.read()
    self.assertEqual(0x60, pushed_value.value)
    self.assertEqual(None, state)

    self.cpu, state = push_pcl_and_decrement_sp(self.cpu)
    self.assertEqual(0x01fb, self.cpu.address_bus.address_word.get())
    self.assertEqual(0xfa, self.cpu.sp().value)
    pushed_value = self.cpu.address_bus.read()
    self.assertEqual(0x02, pushed_value.value)
    self.assertEqual(None, state)

  def test_pull_pc_fxns(self):
    self.cpu.sp(0xea)
    self.cpu.pc(WordValue(0xe632))

    self.cpu.address_bus.set(WordValue(0x1ea))
    self.cpu.address_bus.write(ByteValue(0x40))
    self.cpu.address_bus.set(WordValue(0x1eb))
    self.cpu.address_bus.write(ByteValue(0x80))

    self.cpu, state = pull_pcl_and_increment_sp(self.cpu)
    self.assertEqual(0x01ea, self.cpu.address_bus.address_word.get())
    self.assertEqual(0xeb, self.cpu.sp().value)
    self.assertEqual(0, self.cpu.address_bus.read().value)

    self.assertEqual(0x40, self.cpu.pc().get_lo_byte().value)
    self.assertEqual(0xe6, self.cpu.pc().get_hi_byte().value)
    self.assertEqual(None, state)

    self.cpu, state = pull_pch(self.cpu)
    self.assertEqual(0x01eb, self.cpu.address_bus.address_word.get())
    self.assertEqual(0xeb, self.cpu.sp().value)
    self.assertEqual(0, self.cpu.address_bus.read().value)

    self.assertEqual(0x40, self.cpu.pc().get_lo_byte().value)
    self.assertEqual(0x80, self.cpu.pc().get_hi_byte().value)
    self.assertEqual(True, state)

  def test_push_pull_p(self):
    self.cpu.sp(0xe7)
    self.cpu.pc(WordValue(0x9000))
    self.cpu.p(0b10000100)

    self.cpu, state = push_p_with_b_flag_and_decrement_sp(self.cpu)
    self.assertEqual(0xe6, self.cpu.sp().value)
    self.assertEqual(0x01e7, self.cpu.address_bus.address_word.get())
    p_value_on_stack = self.cpu.address_bus.read()
    self.assertEqual(0b10110100, p_value_on_stack.value)

    # we'll pretend we did something else before we pull P
    self.cpu.p(0b01000010)

    # a real operation would do increment_sp
    # a la brk then plp for some reason
    self.cpu, state = increment_sp(self.cpu)
    self.assertEqual(None, state)

    self.cpu, state = pull_p_and_increment_sp(self.cpu)
    self.assertEqual(0b10000100, self.cpu.p().value)
    self.assertEqual(0xe8, self.cpu.sp().value)
    self.assertEqual(0x01e7, self.cpu.address_bus.address_word.get())
    value_at_bus = self.cpu.address_bus.read()
    self.assertEqual(0, value_at_bus.value)

  def test_pull_push_registers_not_p(self):
    self.cpu.sp(0xe7)
    self.cpu.pc(0x9000)
    self.cpu.a(0x8a)

    self.cpu, state = push_register_decrement_sp(self.cpu, "a")
    self.assertEqual(True, state)
    self.assertEqual(0xe6, self.cpu.sp().value)
    self.assertEqual(0x1e7, self.cpu.address_bus.address_word.get())
    v = self.cpu.address_bus.read()
    self.assertEqual(0x8a, v.value)

    # we'll pretend an operation happened before PLA
    self.cpu.a(0x02)

    self.cpu, state = increment_sp(self.cpu)
    self.assertEqual(None, state)
    self.assertEqual(0xe7, self.cpu.sp().value)
    self.assertEqual(0x1e7, self.cpu.address_bus.address_word.get())

    self.cpu, state = pull_register(self.cpu, "A")

    # pull_register doesn't actually touch the SP by itself
    self.assertEqual(0xe7, self.cpu.sp().value)
    self.assertEqual(0x1e7, self.cpu.address_bus.address_word.get())
    self.assertEqual(0x8a, self.cpu.a().value)
    v = self.cpu.address_bus.read()
    self.assertEqual(0, v.value)





