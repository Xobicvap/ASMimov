
class AddressBus:

  def __init__(self, memory):
    self.memory = memory
    self.address = 0

  def set(self, address):
    self.address = address.get_value()

  def write(self, address, value):
    self.memory.write(address.get_value(), value)

  def read(self):
    self.memory.read(self.address.get_value())
