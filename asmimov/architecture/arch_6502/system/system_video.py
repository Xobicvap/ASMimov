
class SystemVideo:

  # TODO make these a config
  def __init__(self, hblank_mod_value, hblank_length,
               vblank_mod_value, vblank_length):
    self.hblank_mod_value = hblank_mod_value
    self.hblank_length = hblank_length
    self.vblank_mod_value = vblank_mod_value
    self.vblank_length = vblank_length

    self.hblank = False
    self.vblank = False
    self.cycles = 0
    self.in_blank_cycles = 0

  def step(self):
    if self.cycles != 0 and self.cycles % self.hblank_mod_value == 0:
      self.hblank = True
    elif self.cycles != 0 and self.cycles % self.vblank_mod_value == 0:
      self.vblank = True

    if self.hblank:
      if self.in_blank_cycles == self.hblank_length:
        self.hblank = False
        self.in_blank_cycles = 0
      else:
        self.in_blank_cycles = self.in_blank_cycles + 1
    elif self.vblank:
      if self.in_blank_cycles == self.vblank_length:
        self.vblank = False
        self.in_blank_cycles = 0
        self.cycles = 0
      else:
        self.in_blank_cycles = self.in_blank_cycles + 1
    else:
      # somehow, write next pixel
      self.cycles = self.cycles + 1


