class SystemDebug:

  def __init__(self, cpu):
    self.cpu = cpu
    self.halt = True

  def start(self, override_reset=None):
    pass

  def step(self):
    cpu_state = self.cpu.collect_state()
    if not self.halt:
      return
    self.display_cpu_state(**cpu_state)
    user_input = input("* ")

  def display_cpu_state(self, PC, N, V, D, I, Z, C, A, X, Y, P, SP, IR, DR, D2):
    print("PC      NV--DIZC A  X  Y  P  SP IR DR D2")
    print(f'{PC}  {N}{V}--{D}{I}{Z}{C} {A}  {X}  {Y}  {P}  {SP} {IR} {DR} {D2}')
    print("")
