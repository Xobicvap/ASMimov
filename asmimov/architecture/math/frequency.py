
frequency_calc_map = {
  "MHz": 1000000.0,
  "KHz": 1000.0
}

class Frequency:

  def __init__(self, frequency, unit=None):
    if unit is None:
      self.frequency = frequency
    else:
      if unit not in frequency_calc_map:
        raise Exception("Unknown frequency unit")
      self.frequency_human = frequency
      self.frequency = 1 / (frequency * frequency_calc_map[unit])
      self.unit = unit

  def __str__(self):
    print(self.frequency_human + " " + self.unit)

  def __repr__(self):
    print(self.frequency_human + " " + self.unit)

  def __mul__(self, other):
    if isinstance(other, Frequency):
      return Frequency(self.frequency * other.frequency)
    else:
      return Frequency(self.frequency * other)

  def __truediv__(self, other):
    if isinstance(other, Frequency):
      return Frequency(self.frequency / other.frequency)
    else:
      return Frequency(self.frequency / other)

  def value(self):
    return self.frequency

