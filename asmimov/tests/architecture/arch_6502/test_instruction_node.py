from architecture.arch_6502.cpu.instruction_node import InstructionNode
from architecture.arch_6502.cpu.instructions import instruction_tuples as im
from architecture.arch_6502.cpu.cpu_container import CPUContainer
import unittest

class InstructionNodeTest(unittest.TestCase):

  def test_brk(self):
    inst_tuple = im[0x00]
    change_fxn, addr_fxn, op1, op2, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(None, None, None, 0x7000, 0b10001000, 0xff,
                          {0xfffe: 0, 0xffff: 0x80})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0b10001000)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, 0x7000)

    changes = inst.evaluate(system)
    self.assertEqual(changes["SP"], 0xfc)
    self.assertEqual(changes["PC"], 0x8000)
    self.assertEqual(changes[0x1ff], 0x70)
    self.assertEqual(changes[0x1fe], 0x02)
    self.assertEqual(changes[0x1fd], 0b10111000)

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

  def test_php_implied(self):
    inst_tuple = im[0x08]

    change_fxn, addr_fxn, op1, op2, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(None, None, None, 0x7000, 0b10000111, 0xff)

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0x87)
    inst.set_operand2(system, op2)
    self.assertEqual(inst.operand2, None)

    changes = inst.evaluate(system)
    self.assertEqual(changes["SP"], 0xfe)
    status = changes[0x1ff]
    self.assertEqual(status, 0b10110111)
    self.assertEqual(changes["PC"], 0x7001)
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

  def test_bpl(self):
    inst_tuple = im[0x10]

    op1 = 0xd0
    # also remember that the tuple converting function needs to turn "operand"
    # to a value for dest, as well
    change_fxn, addr_fxn, _, op2, dest, pc_disp, cycles = inst_tuple
    inst = InstructionNode(change_fxn, addr_fxn, dest, pc_disp, cycles)
    system = CPUContainer(None, None, None, 0x7000, 0b00001010, 0xff,
                          {0x1423: 0x05})

    inst.set_operand1(system, op1)
    self.assertEqual(inst.operand1, 0xd0)
    inst.set_operand2(system, op2)
    # figure out what to do with status flags
    self.assertEqual(inst.operand2, 0)

    changes = inst.evaluate(system)
    self.assertEqual(changes["PC"], 0x6fd0)
    self.assertEqual(changes["cycles"], 4)


