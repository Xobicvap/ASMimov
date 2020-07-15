from architecture.math.hexnum import WordValue, ByteValue

class AddressBus:

  def __init__(self, memory):
    self.memory = memory
    self.address_word = WordValue(0)

  def set(self, address):
    self.address_word = address if isinstance(address, WordValue) else WordValue(address)

  def write(self, value, address=None):
    # idk if we'll ever use address is not None
    effective_addr = self.address_word if address is None else address
    value = value if isinstance(value, ByteValue) else ByteValue(value)
    self.memory.write(effective_addr.get(), value)

  def read(self):
    return self.memory.read(self.address_word.get())

