import unittest
from architecture.arch_6502.cpu.stack_pointer import StackPointer

class StackPointerTest(unittest.TestCase):

  def test_get_effective(self):
    v1 = StackPointer(0xff)
    self.assertEqual(0x1ff, v1.get_effective().get())
