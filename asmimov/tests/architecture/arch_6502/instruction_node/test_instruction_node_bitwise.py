from architecture.arch_6502.cpu.instruction_node import InstructionNode
from architecture.arch_6502.cpu.instructions import instruction_tuples as im
from architecture.arch_6502.cpu.cpu_container import CPUContainer
import unittest

class BitwiseInstructionNodeTest(unittest.TestCase):
  def test_ora_indexed_indirect(self):
    inst_tuple = im[0x01]
    op2 = 0xd0
    # remember when doing the actual CPU that the inst tuples need
    # a function that converts "operand" in the tuple to whatever the
    # incoming operand is
    change_fxn, addr_fxn, op1, _, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(0x54, 0x10, None, 0x7000, 0b10001000, 0xff,
                          {0xe0: 0x58, 0xe1: 0x90, 0x9058: 0x0b,
                           0xfffe: 0, 0xffff: 0x80})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x54)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, 11)

    changes = inst.evaluate(system)
    self.assertEqual(changes["A"], 0x5f)
    status = changes["P"]
    self.assertEqual(status["N"], 0)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(changes["PC"], 0x7002)
    self.assertEqual(changes["cycles"], 6)

  def test_ora_zero_page(self):
    inst_tuple = im[0x05]
    op2 = 0xe6
    # remember when doing the actual CPU that the inst tuples need
    # a function that converts "operand" in the tuple to whatever the
    # incoming operand is
    change_fxn, addr_fxn, op1, _, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(0x58, None, None, 0x7000, 0b10001000, 0xff,
                          {0xe6: 0x22})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x58)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, 0x22)

    changes = inst.evaluate(system)
    self.assertEqual(changes["A"], 0x7a)
    status = changes["P"]
    self.assertEqual(status["N"], 0)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(changes["PC"], 0x7002)
    self.assertEqual(changes["cycles"], 3)

  def test_ora_immediate(self):
    inst_tuple = im[0x09]
    op2 = 0x86

    change_fxn, addr_fxn, op1, _, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(0x19, None, None, 0x7000, 0b10001000, 0xff)

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x19)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, 0x86)

    changes = inst.evaluate(system)
    self.assertEqual(changes["A"], 0x9f)
    status = changes["P"]
    self.assertEqual(status["N"], 1)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(changes["PC"], 0x7001)
    self.assertEqual(changes["cycles"], 2)

  def test_ora_absolute(self):
    inst_tuple = im[0x0d]
    op2 = 0xcc10
    # remember when doing the actual CPU that the inst tuples need
    # a function that converts "operand" in the tuple to whatever the
    # incoming operand is
    change_fxn, addr_fxn, op1, _, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(0x10, None, None, 0x7000, 0b10001000, 0xff,
                          {0xcc10: 0x9c})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x10)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, 0x9c)

    changes = inst.evaluate(system)
    self.assertEqual(changes["A"], 0x9c)
    status = changes["P"]
    self.assertEqual(status["N"], 1)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(changes["PC"], 0x7003)
    self.assertEqual(changes["cycles"], 4)

