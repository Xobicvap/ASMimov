import unittest
from architecture.math.hexnum import ByteValue, WordValue

class ByteValueTest(unittest.TestCase):

  def test_bit_at(self):
    v = ByteValue(0x80)
    self.assertEqual(1, v.bit_at(7))
    v = ByteValue(0x45)
    self.assertEqual(1, v.bit_at(6))
    v = ByteValue(0x32)
    self.assertEqual(1, v.bit_at(5))
    self.assertEqual(1, v.bit_at(4))
    self.assertEqual(0, v.bit_at(3))
    self.assertEqual(0, v.bit_at(2))
    self.assertEqual(1, v.bit_at(1))
    self.assertEqual(0, v.bit_at(0))

  def test_bit_set(self):
    v = ByteValue(0xa4)
    self.assertTrue(v.bit_set(7))
    self.assertFalse(v.bit_set(6))
    self.assertTrue(v.bit_set(5))
    self.assertFalse(v.bit_set(4))
    self.assertFalse(v.bit_set(3))
    self.assertTrue(v.bit_set(2))
    self.assertFalse(v.bit_set(1))
    self.assertFalse(v.bit_set(0))

  def test_negative(self):
    v = ByteValue(0x7f)
    self.assertFalse(v.negative())

    v = ByteValue(0x81)
    self.assertTrue(v.negative())

  def test_zero(self):
    v = ByteValue(0x05)
    self.assertFalse(v.zero())
    v = ByteValue(0x00)
    self.assertTrue(v.zero())

  def test_add_overloaded(self):
    v1 = ByteValue(0x0b)
    v2 = ByteValue(0x14)
    v3 = v1 + v2

    self.assertEqual(0x1f, v3.value)
    self.assertFalse(v3.carry())

  def test_add_with_overflow(self):
    v1 = ByteValue(0x95)
    v2 = ByteValue(0x96)
    v3 = v1 + v2
    self.assertEqual(0x2b, v3.value)
    self.assertTrue(v3.carry())

  def test_sub_overloaded(self):
    v1 = ByteValue(0x45)
    v2 = ByteValue(0x42)
    v3 = v1 - v2
    self.assertEqual(0x03, v3.value)

  def test_sub_with_overflow(self):
    v1 = ByteValue(0x80)
    v2 = ByteValue(0x81)
    v3 = v1 - v2
    self.assertEqual(0xff, v3.value)

  def test_and(self):
    v1 = ByteValue(0x0f)
    v2 = ByteValue(0xf0)
    v3 = v1 & v2
    self.assertEqual(0x00, v3.value)
    self.assertTrue(v3.zero())

    v2 = ByteValue(0xf5)
    v3 = v1 & v2
    self.assertEqual(0x05, v3.value)

  def test_or(self):
    v1 = ByteValue(0x0f)
    v2 = ByteValue(0xf0)
    v3 = v1 | v2

    self.assertEqual(0xff, v3.value)
    self.assertTrue(v3.negative())

  def test_xor(self):
    # 11101110 ^
    # 11111110 =
    # 00010000
    v1 = ByteValue(0xee)
    v2 = ByteValue(0xfe)
    v3 = v1 ^ v2

    self.assertEqual(0x10, v3.value)
    self.assertFalse(v3.negative())

  def test_lshift_bad_argument(self):
    v1 = ByteValue(0x02)
    with self.assertRaises(Exception):
      v1 << 2

  def test_lshift_no_carry(self):
    v1 = ByteValue(0x42)
    v1 << 1
    self.assertEqual(0x84, v1.value)
    self.assertFalse(v1.carry_happened)

  def test_lshift_carry(self):
    # 10101001 << 1 -> 01010010 (0x52)
    v1 = ByteValue(0xa9)
    v1 << 1
    self.assertEqual(0x52, v1.value)
    self.assertTrue(v1.carry_happened)

  def test_rshift_bad_argument(self):
    v1 = ByteValue(0x02)
    with self.assertRaises(Exception):
      v1 >> 3

  def test_rshift_no_carry(self):
    # 11001110 >> 1 -> 01100111 (0x67)
    v1 = ByteValue(0xce)
    v1 >> 1
    self.assertEqual(0x67, v1.value)
    self.assertFalse(v1.carry_happened)

  def test_rshift_carry(self):
    # 01010011 >> 1 -> 00101001 (1) -> 0x29
    v1 = ByteValue(0x53)
    v1 >> 1
    self.assertEqual(0x29, v1.value)
    self.assertTrue(v1.carry_happened)

  def test_str(self):
    v1 = ByteValue(0x0c)
    self.assertEqual("0C", str(v1))
    v2 = ByteValue(0xfd)
    self.assertEqual("FD", str(v2))

  def test_word_create_overflow_fails(self):
    with self.assertRaises(Exception):
      v1 = WordValue(0x10000)

  def test_word_create_invalid_lo_byte(self):
    with self.assertRaises(Exception):
      v1 = WordValue(0x10000)

  def test_word_create_invalid_hi_byte(self):
    with self.assertRaises(Exception):
      v1 = WordValue(0xff, 0x100)

  def test_word_one_arg_sub_word_right_value(self):
    v1 = WordValue(0xff)
    self.assertEqual(0xff, v1.value)
    self.assertEqual(0xff, v1.get_lo_byte().value)
    self.assertEqual(0x00, v1.get_hi_byte().value)

  def test_word_one_arg_right_value(self):
    v1 = WordValue(0xff30)
    self.assertEqual(0xff30, v1.value)
    self.assertEqual(0x30, v1.get_lo_byte().value)
    self.assertEqual(0xff, v1.get_hi_byte().value)

  def test_word_two_args_right_value(self):
    v1 = WordValue(0x67, 0xc0)
    self.assertEqual(0xc067, v1.value)
    self.assertEqual(0x67, v1.get_lo_byte().value)
    self.assertEqual(0xc0, v1.get_hi_byte().value)

  def test_set_lo_byte_overflow(self):
    v1 = WordValue(0xff00)
    with self.assertRaises(Exception):
      v1.set_lo_byte(0x100)

  def test_set_lo_byte_correct(self):
    v1 = WordValue(0xff00)
    v1.set_lo_byte(0xf0)
    self.assertEqual(0xfff0, v1.value)

  def test_set_hi_byte_overflow(self):
    v1 = WordValue(0xb000)
    with self.assertRaises(Exception):
      v1.set_hi_byte(0x120)

  def test_set_hi_byte_correct(self):
    v1 = WordValue(0x12ff)
    v1.set_hi_byte(0xff)
    self.assertEqual(0xffff, v1.value)

  def test_add_byte_value(self):
    v1 = WordValue(0xe000)
    v2 = v1 + ByteValue(0xff)
    self.assertEqual(0xe0ff, v2.value)

  def test_add_int(self):
    v1 = WordValue(0xd080)
    v2 = v1 + 0x70
    self.assertEqual(0xd0f0, v2.value)

  def test_add_byte_value_overflow(self):
    v1 = WordValue(0x2ffe)
    v2 = v1 + ByteValue(0x03)
    self.assertEqual(0x3001, v2.value)

  def test_add_int_overflow(self):
    v1 = WordValue(0x400f)
    v2 = v1 + 0xf2
    self.assertEqual(0x4101, v2.value)

  def test_sub_byte_value(self):
    v1 = WordValue(0xe000)
    v2 = v1 - ByteValue(0xff)
    self.assertEqual(0xdf01, v2.value)

  def test_sub_int(self):
    v1 = WordValue(0xd080)
    v2 = v1 - 0x70
    self.assertEqual(0xd010, v2.value)

  def test_sub_byte_value_overflow(self):
    v1 = WordValue(0x00d0)
    v2 = v1 - ByteValue(0xe0)
    self.assertEqual(0xfff0, v2.value)

  def test_sub_int_overflow(self):
    v1 = WordValue(0x0022)
    v2 = v1 - 0xff
    self.assertEqual(0xff23, v2.value)



