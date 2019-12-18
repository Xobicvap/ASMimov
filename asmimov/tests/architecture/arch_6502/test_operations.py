import unittest

class OperationsTest(unittest.TestCase):

  class Instruction:
    def __init__(self, tpl, pc_tpl=None):
      self.tpl = tpl
      self.pc_tpl = pc_tpl

    def metadata(self):
      return self.tpl

    def pc_metadata(self):
      return self.pc_tpl
