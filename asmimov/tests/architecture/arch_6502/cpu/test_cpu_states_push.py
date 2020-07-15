import unittest

from architecture.math.hexnum import WordValue, ByteValue
from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_states import *

class CpuStatesPushPullTest(unittest.TestCase):

  def test_increment_pc_no_new_page(self):
    cpu = CPU(Registers(), None)
    cpu.pc(0xf000)

    cpu = increment_pc(cpu)
    self.assertEqual(0xf001, cpu.pc().get())

  def test_increment_pc_new_page(self):
    cpu = CPU(Registers(), None)
    cpu.pc(0xe1ff)

    cpu = increment_pc(cpu)
    self.assertEqual(0xe200, cpu.pc().get())

  def test_increment_sp_no_wrap(self):
    cpu = CPU(Registers(), None)
    cpu.sp(0xfd)

    cpu, state = increment_sp(cpu)
    self.assertEqual(0xfe, cpu.sp().value)
    self.assertEqual(None, state)

  def test_increment_sp_wrap(self):
    cpu = CPU(Registers(), None)
    cpu.sp(0xff)

    cpu, state = increment_sp(cpu)
    self.assertEqual(0x00, cpu.sp().value)
    self.assertEqual(None, state)

  def test_decrement_sp_no_wrap(self):
    cpu = CPU(Registers(), None)
    cpu.sp(0xff)

    cpu, state = decrement_sp(cpu)
    self.assertEqual(0xfe, cpu.sp().value)
    self.assertEqual(None, state)

  def test_decrement_sp_wrap(self):
    cpu = CPU(Registers(), None)
    cpu.sp(0x00)

    cpu, state = decrement_sp(cpu)
    self.assertEqual(0xff, cpu.sp().value)
    self.assertEqual(None, state)

  def test_address_of_stack(self):
    cpu = CPU(Registers(), None)

    cpu.sp(0xff)

    cpu = address_of_stack(cpu)
    address = cpu.address_bus.address_word

    self.assertEqual(0x01ff, address.get())

  def test_push_pc_and_decrement_sp(self):
    cpu = CPU(Registers(), Memory())

    cpu.sp(0xfc)
    cpu.pc(WordValue(0x6002))

    cpu, state = push_pch_and_decrement_sp(cpu)
    self.assertEqual(0x01fc, cpu.address_bus.address_word.get())
    self.assertEqual(0xfb, cpu.sp().value)
    pushed_value = cpu.address_bus.read()
    self.assertEqual(0x60, pushed_value.value)
    self.assertEqual(None, state)

    cpu, state = push_pcl_and_decrement_sp(cpu)
    self.assertEqual(0x01fb, cpu.address_bus.address_word.get())
    self.assertEqual(0xfa, cpu.sp().value)
    pushed_value = cpu.address_bus.read()
    self.assertEqual(0x02, pushed_value.value)
    self.assertEqual(None, state)

  def test_pull_pc_fxns(self):
    cpu = CPU(Registers(), Memory())

    cpu.sp(0xea)
    cpu.pc(WordValue(0xe632))

    cpu.address_bus.set(WordValue(0x1ea))
    cpu.address_bus.write(ByteValue(0x40))
    cpu.address_bus.set(WordValue(0x1eb))
    cpu.address_bus.write(ByteValue(0x80))

    cpu, state = pull_pcl_and_increment_sp(cpu)
    self.assertEqual(0x01ea, cpu.address_bus.address_word.get())
    self.assertEqual(0xeb, cpu.sp().value)
    self.assertEqual(0, cpu.address_bus.read().value)

    self.assertEqual(0x40, cpu.pc().get_lo_byte().value)
    self.assertEqual(0xe6, cpu.pc().get_hi_byte().value)
    self.assertEqual(None, state)

    cpu, state = pull_pch(cpu)
    self.assertEqual(0x01eb, cpu.address_bus.address_word.get())
    self.assertEqual(0xeb, cpu.sp().value)
    self.assertEqual(0, cpu.address_bus.read().value)

    self.assertEqual(0x40, cpu.pc().get_lo_byte().value)
    self.assertEqual(0x80, cpu.pc().get_hi_byte().value)
    self.assertEqual(True, state)

  def test_push_pull_p(self):
    cpu = CPU(Registers(), Memory())

    cpu.sp(0xe7)
    cpu.pc(WordValue(0x9000))
    cpu.p(0b10000100)

    cpu, state = push_p_with_b_flag_and_decrement_sp(cpu)
    self.assertEqual(0xe6, cpu.sp().value)
    self.assertEqual(0x01e7, cpu.address_bus.address_word.get())
    p_value_on_stack = cpu.address_bus.read()
    self.assertEqual(0b10110100, p_value_on_stack.value)

    # we'll pretend we did something else before we pull P
    cpu.p(0b01000010)

    # a real operation would do increment_sp
    # a la brk then plp for some reason
    cpu, state = increment_sp(cpu)
    self.assertEqual(None, state)

    cpu, state = pull_p_and_increment_sp(cpu)
    self.assertEqual(0b10000100, cpu.p().value)
    self.assertEqual(0xe8, cpu.sp().value)
    self.assertEqual(0x01e7, cpu.address_bus.address_word.get())
    value_at_bus = cpu.address_bus.read()
    self.assertEqual(0, value_at_bus.value)

  def test_pull_push_registers_not_p(self):
    cpu = CPU(Registers(), Memory())

    cpu.sp(0xe7)
    cpu.pc(0x9000)
    cpu.a(0x8a)

    cpu, state = push_register_decrement_sp(cpu, "a")
    self.assertEqual(True, state)
    self.assertEqual(0xe6, cpu.sp().value)
    self.assertEqual(0x1e7, cpu.address_bus.address_word.get())
    v = cpu.address_bus.read()
    self.assertEqual(0x8a, v.value)

    # we'll pretend an operation happened before PLA
    cpu.a(0x02)

    cpu, state = increment_sp(cpu)
    self.assertEqual(None, state)
    self.assertEqual(0xe7, cpu.sp().value)
    self.assertEqual(0x1e7, cpu.address_bus.address_word.get())

    cpu, state = pull_register(cpu, "A")

    # pull_register doesn't actually touch the SP by itself
    self.assertEqual(0xe7, cpu.sp().value)
    self.assertEqual(0x1e7, cpu.address_bus.address_word.get())
    self.assertEqual(0x8a, cpu.a().value)
    v = cpu.address_bus.read()
    self.assertEqual(0, v.value)





