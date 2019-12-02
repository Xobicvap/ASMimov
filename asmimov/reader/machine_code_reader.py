import os

class MachineCodeReader:

  def __init__(self, opcode_tuples, offset = 0, stop_at = None):
    self._opcode_map = opcode_tuples
    self._offset = offset
    self._stop_at = stop_at

  def _convert_byte_to_hex_string(self, byte):
    tempstr = str(hex(byte)).replace("0x", "")
    if byte < 16:
      tempstr = "0" + tempstr
    return tempstr.upper()

  def _get_opcode_tuple(self, opcode):
    if opcode not in self._opcode_map:
      return (".db $" + self._convert_byte_to_hex_string(opcode), 0, "")
    return self._opcode_map[opcode]

  def _convert_operands(self, operands):
    if len(operands) == 1:
      return self._convert_byte_to_hex_string(operands[0])
    if len(operands) == 2:
      lobyte = self._convert_byte_to_hex_string(operands[0])
      hibyte = self._convert_byte_to_hex_string(operands[1])
      hexword = hibyte + lobyte
      return hexword

  def _make_opcode(self, opcode, template, replace_str, operands):
    return opcode + " " + template.replace(replace_str, self._convert_operands(operands))

  def _read_opcode(self, opcode, operands, template):
    if len(operands) == 0 and len(template) == 0:
      return opcode
    if len(operands) == 0 and template == "A":
      return opcode + " " + template
    if "BB" in template and len(operands) == 1:
      return self._make_opcode(opcode, template, "BB", operands)
    if "LL" in template and len(operands) == 1:
      return self._make_opcode(opcode, template, "LL", operands)
    if "HHLL" in template and len(operands) == 2:
      return self._make_opcode(opcode, template, "HHLL", operands)
    raise Exception("unreadable opcode: " + opcode + " " + template + ".. " + str(len(operands)))

  def disassemble(self, binarr):
    lines = []
    done_reading = False
    offset = self._offset
    stop_at = self._stop_at

    while not done_reading:
      current_byte = binarr[offset]

      opcode, bytect, template = self._get_opcode_tuple(current_byte)
      ptr = offset + bytect + 1
      nextbyte = offset + 1
      operands = binarr[nextbyte:ptr]

      instruction = self._read_opcode(opcode, operands, template)

      line = "  " + instruction
      offset = offset + bytect + 1
      lines.append(line)
      if offset >= len(binarr):
        done_reading = True
      elif stop_at is not None and offset >= stop_at:
        done_reading = True
    return lines

