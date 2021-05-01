class SystemDebug:

  def __init__(self, cpu):
    self.cpu = cpu
    self.halt = False
    self.breakpoint = 0xfc10

  def start(self, override_reset=None):
    pass

  def step(self):
    cpu_state = self.cpu.collect_state()
    self.display_cpu_state(**cpu_state)
    try:
      if self.cpu.pc().value == self.breakpoint:
        self.halt = True
    except Exception:
      if self.cpu.pc() == self.breakpoint:
        self.halt = True
    if not self.halt:
      return
    resume = False
    while not resume:
      menu_result = self.menu(input("* "))
      resume = True if menu_result == "g" else False

  def display_cpu_state(self, PC, N, V, D, I, Z, C, A, X, Y, P, SP, IR, DR, D2):
    print("PC      NV--DIZC A  X  Y  P  SP IR DR D2")
    print(f'{PC}  {N}{V}--{D}{I}{Z}{C} {A} {X} {Y} {P} {SP} {IR} {DR} {D2}')
    print("")

  def menu(self, user_input):
    normalized = user_input.lower()
    args = normalized.split(" ")
    if args[0] == "p":
      self.show_page(args[1])
    elif args[0] == "g":
      self.halt = False
      return args[0]

  def show_page(self, pagenum):
    hex_str = "0x" + pagenum + "00"
    page = int(hex_str, 16)
    print("       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
    start = "       "
    bytes_line = start
    for i in range(page, page + 0x100):
      mem = self.cpu.address_bus.memory.read(i)
      bytes_line += str(mem).replace("0x", "") + " "
      if i % 16 == 0 and i != 0:
        print(bytes_line)
        bytes_line = start
