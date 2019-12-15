import unittest

class OperationsTest(unittest.TestCase):

  class Instruction:
    def __init__(self, tpl):
      self.tpl = tpl

    def metadata(self):
      return self.tpl

