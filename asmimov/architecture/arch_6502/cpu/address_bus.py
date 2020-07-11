
class AddressBus:

  def __init__(self, memory):
    self.memory = memory
    self.address = 0
    self.address_word = WordValue(0)

  def set(self, address):
    self.address = address.get()
    self.address_word = address

  def write(self, value, address=None):
    # idk if we'll ever use address is not None
    effective_addr = self.address if address is None else address
    self.memory.write(effective_addr, value)

  def read(self):
    self.memory.read(self.address)
