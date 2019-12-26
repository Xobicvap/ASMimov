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

  class TestSystem:
    def __init__(self, statuses={}, memory={}, vectors={}):
      self.statuses = statuses
      self.memory = memory
      self.vectors = vectors

    def status(self, x):
      return self.statuses[x]

    def read_direct(self, addr):
      return self.memory[addr]

    def read_direct_absolute(self, addr):
      addr_byte_lo = self.read_direct(addr)
      addr_byte_hi = self.read_direct(addr + 1)
      return (addr_byte_hi << 8) + addr_byte_lo

    def vector(self, name):
      return self.read_direct_absolute(self.vectors[name])
 

