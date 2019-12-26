import unittest
from tests.architecture.arch_6502 import test_operations
from architecture.arch_6502 import operations

class OperationsTransferIncrementDecrementTest(test_operations.OperationsTest):

  def test_dex_no_overflow_positive_nonzero(self):
    metadata = (0x80, None, 'X')
    self.decrement_test(metadata, operations.dex, 0, 0)

  def test_dex_no_overflow_negative(self):
    metadata = (0x81, None, 'X')
    self.decrement_test(metadata, operations.dex, 0, 1)

  def test_dex_zero(self):
    metadata = (0x01, None, 'X')
    self.decrement_test(metadata, operations.dex, 1, 0)

  def test_dex_overflow_negative(self):
    metadata = (0x00, None, 'X')
    self.decrement_test(metadata, operations.dex, 0, 1)

  def test_dey_no_overflow_positive_nonzero(self):
    metadata = (0x70, None, 'Y')
    self.decrement_test(metadata, operations.dey, 0, 0)

  def test_dey_no_overflow_negative(self):
    metadata = (0x82, None, 'Y')
    self.decrement_test(metadata, operations.dey, 0, 1)

  def test_dey_zero(self):
    metadata = (0x01, None, 'Y')
    self.decrement_test(metadata, operations.dey, 1, 0)

  def test_dey_overflow_negative(self):
    metadata = (0x00, None, 'Y')
    self.decrement_test(metadata, operations.dey, 0, 1)

  def test_dec_no_overflow_positive_nonzero(self):
    metadata = (0x60, None, 0x4000)
    self.decrement_test(metadata, operations.dec, 0, 0)

  def test_dec_no_overflow_negative(self):
    metadata = (0xa2, None, 0x4000)
    self.decrement_test(metadata, operations.dec, 0, 1)

  def test_dec_zero(self):
    metadata = (0x01, None, 0x4000)
    self.decrement_test(metadata, operations.dec, 1, 0)

  def test_dec_overflow_negative(self):
    metadata = (0x00, None, 0x4000)
    self.decrement_test(metadata, operations.dec, 0, 1)

  def test_inx_no_overflow_positive_nonzero(self):
    metadata = (0x7e, None, 'X')
    self.increment_test(metadata, operations.inx, 0, 0)

  def test_inx_no_overflow_negative(self):
    metadata = (0x81, None, 'X')
    self.increment_test(metadata, operations.inx, 0, 1)

  def test_inx_overflow_zero(self):
    metadata = (0xff, None, 'X')
    self.increment_test(metadata, operations.inx, 1, 0)

  def test_iny_no_overflow_positive_nonzero(self):
    metadata = (0x70, None, 'Y')
    self.increment_test(metadata, operations.iny, 0, 0)

  def test_iny_no_overflow_negative(self):
    metadata = (0x82, None, 'Y')
    self.increment_test(metadata, operations.iny, 0, 1)

  def test_iny_overflow_zero(self):
    metadata = (0xff, None, 'Y')
    self.increment_test(metadata, operations.iny, 1, 0)

  def test_inc_no_overflow_positive_nonzero(self):
    metadata = (0x60, None, 0x4000)
    self.increment_test(metadata, operations.inc, 0, 0)

  def test_inc_no_overflow_negative(self):
    metadata = (0xa2, None, 0x4000)
    self.increment_test(metadata, operations.inc, 0, 1)

  def test_inc_overflow_zero(self):
    metadata = (0xff, None, 0x4000)
    self.increment_test(metadata, operations.inc, 1, 0)

  def decrement_test(self, metadata, op, expect_z, expect_n):
    v, _, dest = metadata
    inst = self.Instruction(metadata)

    result = op(None, inst)
    dest_val = result[dest]
    if v == 0:
      self.assertEqual(dest_val, 0xff)
    else:
      self.assertEqual(dest_val, v - 1)
    status = result["P"]
    z = status["Z"]
    n = status["N"]
    self.assertEqual(z, expect_z)
    self.assertEqual(n, expect_n)

  def increment_test(self, metadata, op, expect_z, expect_n):
    v, _, dest = metadata
    inst = self.Instruction(metadata)

    result = op(None, inst)
    dest_val = result[dest]
    if v == 0xff:
      self.assertEqual(dest_val, 0x00)
    else:
      self.assertEqual(dest_val, v + 1)
    status = result["P"]
    z = status["Z"]
    n = status["N"]
    self.assertEqual(z, expect_z)
    self.assertEqual(n, expect_n)

  #def transfer_test(self):
