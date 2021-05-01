from config.system_config import SystemConfig
from run.runner_generator import RunnerGenerator
from architecture.arch_6502.system.emulated_system import EmulatedSystem
from file_ops.file_reader import FileReader
import sys

class AsmimovRunner:

  def __init__(self, rom_file, override_reset=None):
    configuration = SystemConfig()
    runner = RunnerGenerator()
    systems = runner.generate(configuration)
    self.emulation = EmulatedSystem(systems)
    rom_data = FileReader(rom_file, "/home/rusty.hamilton/projects/python/asmimov2/data/").read_file()
    rom_length = len(rom_data)
    if rom_length > 65535:
      raise Exception("Cannot handle ROMs larger than 64K")
    offset = 65536 - rom_length
    rom_mem = {}
    for i in rom_data:
      rom_mem[offset] = i
      offset += 1
    self.emulation.get_cpu_state().address_bus.memset(rom_mem)

    self.emulation.start()

  def run(self):
    continuing = True
    while continuing:
      self.emulation.step()
    print("Thank you for using ASMIMOV.")


if __name__ == "__main__":
  rom_file_path = sys.argv[1]
  override_reset = sys.argv[2] if len(sys.argv) == 3 else None
  runner = AsmimovRunner(rom_file_path, override_reset)
  runner.run()






