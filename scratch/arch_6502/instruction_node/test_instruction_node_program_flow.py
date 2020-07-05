from architecture.arch_6502.cpu.instruction_node import InstructionNode
from architecture.arch_6502.cpu.instructions import instruction_tuples as im
from architecture.arch_6502.cpu.cpu_container import CPUContainer
import unittest

class ProgramFlowInstructionNodeTest(unittest.TestCase):

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