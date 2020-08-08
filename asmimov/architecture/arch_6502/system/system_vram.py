
class SystemVRAM:

  def __init__(self, horiz_res, vert_res):
    self.vram = {}
    for y in range(0, vert_res):
      for x in range(0, horiz_res):
        self.vram[(x, y)] = 0

  def step(self):