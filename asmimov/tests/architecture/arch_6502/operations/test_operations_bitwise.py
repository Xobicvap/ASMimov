import unittest
from tests.architecture.arch_6502.operations import test_operations
from architecture.arch_6502.cpu import operations

class OperationsBitwiseLogicTest(test_operations.OperationsTest):

    and_numbers = [
      # tests that and with 0xff produces same number  
      ((0x1e, 0xff, 'A'), (0x1e, 0, 0)),
      
      # next three tests test that and works properly at all
      ((0x21, 0x20, 'A'), (0x20, 0, 0)),
      ((0x78, 0x54, 'A'), (0x50, 0, 0)),
      ((0xa2, 0x22, 'A'), (0x22, 0, 0)),

      # tests that the zero flag is set 
      ((0x7f, 0x80, 'A'), (0x00, 0, 1)),

      # tests that the negative flag is set
      ((0xde, 0x84, 'A'), (0x84, 1, 0))
    ]

    ora_numbers = [
      # tests that or with 0xff produces 0xff
      ((0x62, 0xff, 'A'), (0xff, 1, 0)),
      
      # next three tests test or operation in general
      ((0x32, 0x41, 'A'), (0x73, 0, 0)),
      ((0x1f, 0x61, 'A'), (0x7f, 0, 0)),
      ((0x02, 0x08, 'A'), (0x0a, 0, 0)),

      # tests that the zero flag is set
      ((0x00, 0x00, 'A'), (0x00, 0, 1)),

      # tests that the negative flag is set
      ((0x72, 0x95, 'A'), (0xf7, 1, 0))
    ]

    eor_numbers = [
      # next three tests test eor operation in general
      ((0x62, 0x1e, 'A'), (0x7c, 0, 0)),
      ((0x19, 0x5b, 'A'), (0x42, 0, 0)),
      ((0x03, 0x3a, 'A'), (0x39, 0, 0)),

      # tests that the zero flag is set
      ((0x00, 0x00, 'A'), (0x00, 0, 1)),
      ((0xee, 0xee, 'A'), (0x00, 0, 1)),

      # tests that the negative flag is set
      ((0x76, 0x99, 'A'), (0xef, 1, 0))
    ]

    def test_and(self):
      test_cases = self.and_numbers

      for tc in test_cases:
        metadata, results = tc
        inst = self.Instruction(metadata)
        v, n, z = results

        result = operations.logical_and(None, inst)

        dv = result["A"]
        dp = result["P"]
        dz = dp["Z"]
        dn = dp["N"]

        self.assertEqual(dv, v)
        self.assertEqual(dn, n)
        self.assertEqual(dz, z)

    def test_or(self):
      test_cases = self.ora_numbers

      for tc in test_cases:
        metadata, results = tc
        inst = self.Instruction(metadata)
        v, n, z = results

        result = operations.ora(None, inst)

        dv = result["A"]
        dp = result["P"]
        dz = dp["Z"]
        dn = dp["N"]

        self.assertEqual(dv, v)
        self.assertEqual(dn, n)
        self.assertEqual(dz, z)

    def test_eor(self):
      test_cases = self.eor_numbers

      for tc in test_cases:
        metadata, results = tc
        inst = self.Instruction(metadata)
        v, n, z = results

        result = operations.eor(None, inst)

        dv = result["A"]
        dp = result["P"]
        dz = dp["Z"]
        dn = dp["N"]

        self.assertEqual(dv, v)
        self.assertEqual(dn, n)
        self.assertEqual(dz, z)

    def test_bit_negative_flag_set_in_memory_location(self):
      metadata = (0x80, 0x80, None)
      inst = self.Instruction(metadata)

      result = operations.bit(None, inst)

      dp = result["P"]
      dz = dp["Z"]
      dn = dp["N"]
      dv = dp["V"]

      self.assertEqual(dz, 0)
      self.assertEqual(dn, 1)
      self.assertEqual(dv, 0)

    def test_bit_zero_flag_set_from_anding_mem_with_acc(self):
      metadata = (0x01, 0x20, 'A')
      inst = self.Instruction(metadata)

      result = operations.bit(None, inst)

      dp = result["P"]
      dz = dp["Z"]
      dn = dp["N"]
      dv = dp["V"]

      self.assertEqual(dz, 1)
      self.assertEqual(dn, 0)
      self.assertEqual(dv, 0)

    def test_bit_overflow_flag_set_in_memory_location(self):
      metadata = (0x61, 0x43, 'A')
      inst = self.Instruction(metadata)

      result = operations.bit(None, inst)

      dp = result["P"]
      dz = dp["Z"]
      dn = dp["N"]
      dv = dp["V"]

      self.assertEqual(dz, 0)
      self.assertEqual(dn, 0)
      self.assertEqual(dv, 1)

