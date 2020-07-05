import unittest
import architecture.arch_6502.cpu.cpu_container

class OperationsTest(unittest.TestCase):

  # we're mocking these in this test base because we don't really care what
  # the underlying implementation is
  class Instruction:
    def __init__(self, tpl, pc_tpl=None):
      self.tpl = tpl
      if pc_tpl is not None:
        temp = list(self.tpl)
        temp_pc_tpl = list(pc_tpl)
        temp.extend(temp_pc_tpl)
        self.tpl = tuple(temp)

    def metadata(self):
      return self.tpl

    def pc_metadata(self, cpu_container):
      return self.tpl
