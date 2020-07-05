
class Instruction:

  def __init__(self, *operands):
    if len(operands) == 0:
      raise ValueError("NO INSTRUCTION TAKES 0 OPCODES")

    if len(operands) > 1:
      inst_operands = operands[1:]
      for idx, operand in enumerate(inst_operands):
        i = idx + 1
        operand_name = "operand" + str(i)
        setattr(self, operand_name, operand)

    self.opcode = operands[0]
