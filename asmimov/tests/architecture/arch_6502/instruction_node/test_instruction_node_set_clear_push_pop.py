from architecture.arch_6502.cpu.instruction_node import InstructionNode
from architecture.arch_6502.cpu.instructions import instruction_tuples as im
from architecture.arch_6502.cpu.cpu_container import CPUContainer
import unittest

class SetClearPushPopInstructionNodeTest(unittest.TestCase):

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