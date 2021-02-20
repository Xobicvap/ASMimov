import unittest

from architecture.arch_6502.system.system_cpu import SystemCPU
from architecture.arch_6502.cpu.cpu import CPU
from architecture.arch_6502.cpu.registers import Registers
from architecture.arch_6502.cpu.memory import Memory
from architecture.arch_6502.cpu.cpu_cycle_fxns import *

# this one DOES NOT test aggregation!
class SystemCpuTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.cpu = CPU(Registers(), Memory())

  def test_brk(self):
    cpu = self.cpu

    cpu.sp(0xff)
    cpu.p(0b10000101)
    cpu.pc(0x8001)

    cpu.address_bus.memset({
      0x8001: 0x00,
      0x8002: 0x78,
      0xfffe: 0x02,
      0xffff: 0x81
    })

    sys = SystemCPU(cpu)
    sys.step()
    self.assertEqual(0x00, sys.cpu.IR().value)
    self.assertEqual(0x8002, sys.cpu.pc().value)
    self.assertEqual(6, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(0x8102, sys.cpu.pc().value)

    sys.cpu.address_set(0x1ff)
    self.assertEqual(0x80, sys.cpu.address_read().value)
    sys.cpu.address_set(0x1fe)
    self.assertEqual(0x03, sys.cpu.address_read().value)
    sys.cpu.address_set(0x1fd)
    self.assertEqual(0xb5, sys.cpu.address_read().value)
    self.assertEqual(0xfc, sys.cpu.sp().value)
    self.assertEqual(0x85, sys.cpu.p().value)
    self.assertEqual(0x8102, sys.cpu.pc().value)
    self.assertEqual(7, sys.cycles)

  def test_ora_indexed_indirect(self):
    cpu = self.cpu

    cpu.pc(0xfc00)
    cpu.x(0x80)
    cpu.a(0xe0)

    cpu.address_bus.memset({
      0xfc00: 0x01,
      0xfc01: 0x78,
      0x00f8: 0x05,
      0x00f9: 0x02,
      0x0205: 0x0e
    })

    sys = SystemCPU(cpu)
    sys.step()
    self.assertEqual(0x01, sys.cpu.IR().value)
    self.assertEqual(0xfc01, sys.cpu.pc().value)
    self.assertEqual(5, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(0xfc02, sys.cpu.pc().value)
    self.assertEqual(0xee, sys.cpu.a().value)
    self.assertEqual(6, sys.cycles)

  def test_ora_zp(self):
    cpu = self.cpu

    cpu.pc(0x9ccc)
    cpu.a(0x0e)

    cpu.address_bus.memset({
      0x9ccc: 0x05,
      0x9ccd: 0x89,
      0x0089: 0xa1
    })

    sys = SystemCPU(cpu)
    sys.step()
    self.assertEqual(0x05, sys.cpu.IR().value)
    self.assertEqual(0x9ccd, sys.cpu.pc().value)
    self.assertEqual(2, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(3, sys.cycles)
    self.assertEqual(0x9cce, sys.cpu.pc().value)
    self.assertEqual(0xaf, sys.cpu.a().value)

  def test_asl_zp(self):
    cpu = self.cpu

    cpu.pc(0xae4b)
    cpu.a(0x0e)

    cpu.address_bus.memset({
      0xae4b: 0x06,
      0xae4c: 0x62,
      0x0062: 0x15
    })

    sys = SystemCPU(cpu)
    sys.step()
    self.assertEqual(0x06, sys.cpu.IR().value)
    self.assertEqual(0xae4c, sys.cpu.pc().value)
    self.assertEqual(4, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    i = 0
    while len(sys.current_steps) > 0:
      sys.step()
      if i == 2:
        self.assertEqual(0x2a, sys.cpu.DR().value)
      i = i + 1
    self.assertEqual(5, sys.cycles)
    self.assertEqual(0xae4d, sys.cpu.pc().value)
    sys.cpu.address_set(0x0062)
    v = sys.cpu.address_read()
    self.assertEqual(0x2a, v.value)

  def test_php(self):
    cpu = self.cpu

    cpu.pc(0x8000)
    cpu.p(0b11000001)

    cpu.sp(0xdf)
    cpu.address_bus.memset({
      0x8000: 0x08
    })

    sys = SystemCPU(cpu)
    sys.step()

    self.assertEqual(0x08, sys.cpu.IR().value)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    self.assertEqual(2, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(3, sys.cycles)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    sys.cpu.address_set(0x1df)
    v = sys.cpu.address_read()
    self.assertEqual(0b11110001, v.value)

  def test_ora_immediate(self):
    cpu = self.cpu

    cpu.pc(0x8000)
    cpu.a(0b10001010)

    cpu.sp(0xff)
    cpu.address_bus.memset({
      0x8000: 0x09,
      0x8001: 0b111
    })

    sys = SystemCPU(cpu)
    sys.step()

    self.assertEqual(0x09, sys.cpu.IR().value)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    self.assertEqual(1, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(2, sys.cycles)
    self.assertEqual(0x8002, sys.cpu.pc().value)
    self.assertEqual(0b10001111, sys.cpu.a().value)

  def test_asl_implied(self):
    cpu = self.cpu

    cpu.pc(0x8000)
    cpu.a(0b10001010)

    cpu.sp(0xff)
    cpu.address_bus.memset({
      0x8000: 0x0a
    })

    sys = SystemCPU(cpu)
    sys.step()

    self.assertEqual(0x0a, sys.cpu.IR().value)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    self.assertEqual(1, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(2, sys.cycles)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    self.assertEqual(0b00010100, sys.cpu.a().value)
    self.assertEqual(1, sys.cpu.c())

  def test_ora_absolute(self):
    cpu = self.cpu

    cpu.pc(0x8000)
    cpu.a(0b10001010)

    cpu.sp(0xff)

    cpu.address_bus.memset({
      0x8000: 0x0d,
      0x8001: 0x33,
      0x8002: 0x06,
      0x0633: 0b00100100
    })

    sys = SystemCPU(cpu)
    sys.step()

    self.assertEqual(0x0d, sys.cpu.IR().value)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    self.assertEqual(3, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(4, sys.cycles)
    self.assertEqual(0x8003, sys.cpu.pc().value)
    self.assertEqual(0b10101110, sys.cpu.a().value)

  def test_asl_absolute(self):
    cpu = self.cpu

    cpu.pc(0x8000)
    cpu.sp(0xff)
    cpu.address_bus.memset({
      0x8000: 0x0e,
      0x8001: 0x33,
      0x8002: 0x06,
      0x0633: 0b11000011
    })

    sys = SystemCPU(cpu)
    sys.step()

    self.assertEqual(0x0e, sys.cpu.IR().value)
    self.assertEqual(0x8001, sys.cpu.pc().value)
    self.assertEqual(5, len(sys.current_steps))
    self.assertEqual(1, sys.cycles)

    while len(sys.current_steps) > 0:
      sys.step()
    self.assertEqual(6, sys.cycles)
    self.assertEqual(0x8003, sys.cpu.pc().value)
    sys.cpu.address_set(0x0633)
    v = sys.cpu.address_read()

    self.assertEqual(0b10000110, v.value)
    self.assertEqual(1, sys.cpu.c())

  def test_bpl_no_branch(self):