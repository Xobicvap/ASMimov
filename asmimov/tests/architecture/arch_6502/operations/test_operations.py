import unittest
import architecture.arch_6502.cpu.cpu_container

class OperationsTest(unittest.TestCase):

  # we're mocking these in this test base because we don't really care what
  # the underlying implementation is
  class Instruction:
    def __init__(self, tpl, pc_tpl=None):
      self.tpl = tpl
      self.pc_tpl = pc_tpl

    def metadata(self):
      return self.tpl

    def pc_metadata(self):
      return self.pc_tpl
