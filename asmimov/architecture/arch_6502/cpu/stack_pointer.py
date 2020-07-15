from architecture.math.hexnum import ByteValue, WordValue

class StackPointer(ByteValue):

  def __init__(self, v):
    if isinstance(v, ByteValue):
      self.value = v.value
    else:
      self.value = v
    self.effective_address = 0x100

  def get_effective(self):
    return WordValue(self, 0x01)
