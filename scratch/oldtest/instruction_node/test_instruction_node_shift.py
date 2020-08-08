from architecture.arch_6502.cpu.instruction_node import InstructionNode
from architecture.arch_6502.cpu.instructions import instruction_tuples as im
from architecture.arch_6502.cpu.cpu_container import CPUContainer
import unittest

class ShiftInstructionNodeTest(unittest.TestCase):
  def test_asl_zero_page(self):
    inst_tuple = im[0x06]

    op1 = 0x14
    # also remember that the tuple converting function needs to turn "operand"
    # to a value for dest, as well
    change_fxn, addr_fxn, _, op2, _, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, op1, pc_disp, cycles)
    system = CPUContainer(None, None, None, 0x7000, 0b10001000, 0xff,
                          {0x14: 0xb4})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0xb4)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, None)

    changes = inst.evaluate(system)
    self.assertEqual(changes[0x14], 0x68)  # 10110100 << = 01101000
    status = changes["P"]
    self.assertEqual(status["N"], 0)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(status["C"], 1)
    self.assertEqual(changes["PC"], 0x7002)
    self.assertEqual(changes["cycles"], 5)

  def test_asl_immediate(self):
    inst_tuple = im[0x0a]

    change_fxn, addr_fxn, op1, op2, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(0x2c, None, None, 0x7000, 0b10001000, 0xff)

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x2c)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, None)

    changes = inst.evaluate(system)
    self.assertEqual(changes["A"], 0x58)
    status = changes["P"]
    self.assertEqual(status["N"], 0)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(changes["PC"], 0x7001)
    self.assertEqual(changes["cycles"], 2)

  def test_asl_absolute(self):
    inst_tuple = im[0x0e]

    op1 = 0x1423
    # also remember that the tuple converting function needs to turn "operand"
    # to a value for dest, as well
    change_fxn, addr_fxn, _, op2, _, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, op1, pc_disp, cycles)
    system = CPUContainer(None, None, None, 0x7000, 0b10001000, 0xff,
                          {0x1423: 0x05})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x05)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, None)

    changes = inst.evaluate(system)
    self.assertEqual(changes[0x1423], 0x0a)
    status = changes["P"]
    self.assertEqual(status["N"], 0)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(status["C"], 0)
    self.assertEqual(changes["PC"], 0x7003)
    self.assertEqual(changes["cycles"], 4)

  def test_asl_zero_page_x(self):
    inst_tuple = im[0x16]

    op1 = 0x1e
    # also remember that the tuple converting function needs to turn "operand"
    # to a value for dest, as well
    change_fxn, addr_fxn, _, op2, _, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, op1, pc_disp, cycles)
    system = CPUContainer(None, 0x57, None, 0x7000, 0b10001000, 0xff,
                          {0x75: 0x59, 0x1e: 0x02})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x75)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, None)

    changes = inst.evaluate(system)
    self.assertEqual(changes[0x75], 0xb2)
    status = changes["P"]
    self.assertEqual(status["N"], 1)
    self.assertEqual(status["Z"], 0)
    self.assertEqual(status["C"], 0)
    self.assertEqual(changes["PC"], 0x7002)
    self.assertEqual(changes["cycles"], 6)
