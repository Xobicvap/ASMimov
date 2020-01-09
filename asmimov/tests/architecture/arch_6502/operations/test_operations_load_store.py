import unittest
from tests.architecture.arch_6502.operations import test_operations
from architecture.arch_6502.cpu import operations

class OperationsLoadStoreTest(test_operations.OperationsTest):

  def test_sta(self):
    metadata = (0x77, None, 0x0a)
    self.store_test(metadata, operations.sta)

  def test_stx(self):
    metadata = (0xb5, None, 0x2000)
    self.store_test(metadata, operations.stx)

  def test_sty(self):
    metadata = (0xfe, None, 0x33ff)
    self.store_test(metadata, operations.sty)

  def test_lda_positive_nonzero(self):
    metadata = (0x65, None, "A")
    self.load_test(metadata, operations.lda, 0, 0)

  def test_lda_zero(self):
    metadata = (0x00, None, "A")
    self.load_test(metadata, operations.lda, 1, 0)

  def test_lda_negative(self):
    metadata = (0x98, None, "A")
    self.load_test(metadata, operations.lda, 0, 1)

  def test_ldx_positive_nonzero(self):
    metadata = (0x7f, None, "X")
    self.load_test(metadata, operations.ldx, 0, 0)

  def test_ldx_zero(self):
    metadata = (0x00, None, "X")
    self.load_test(metadata, operations.ldx, 1, 0)

  def test_ldx_negative(self):
    metadata = (0xc4, None, "X")
    self.load_test(metadata, operations.ldx, 0, 1)

  def test_ldy_positive_nonzero(self):
    metadata = (0x24, None, "Y")
    self.load_test(metadata, operations.ldy, 0, 0)

  def test_ldy_zero(self):
    metadata = (0x00, None, "Y")
    self.load_test(metadata, operations.ldy, 1, 0)

  def test_ldy_negative(self):
    metadata = (0xbc, None, "Y")
    self.load_test(metadata, operations.ldy, 0, 1)

  def store_test(self, metadata, op):
    src, _, dest = metadata
    inst = self.Instruction(metadata)

    result = op(None, inst)

    mem = result[dest]
    self.assertEqual(mem, src)

  def load_test(self, metadata, op, expect_zero, expect_n):
    src, _, dest = metadata
    inst = self.Instruction(metadata)
    result = op(None, inst)

    mem = result[dest]
    status = result["P"]
    self.assertEqual(mem, src)
    z = status["Z"]
    n = status["N"]
    self.assertEqual(z, expect_zero)
    self.assertEqual(n, expect_n)
