from file_ops import file_reader, file_writer
from reader import machine_code_reader
from sys import argv
from architecture.arch_6502 import opcodes

if __name__ == "__main__":
  if len(argv) < 3 or len(argv) > 6:
    print("Usage: runner.py (6502 file) (asm file) [path] [offset] [bytes to read]")
    exit()
  binfile = argv[1]
  asmfile = argv[2]
  supplied_path = None
  offset = 0
  stop_at = None
  if len(argv) > 3:
    supplied_path = argv[3]
    if supplied_path[-1] is not '/':
      supplied_path = supplied_path + '/'
    
    if len(argv) > 4:
      offset = int(argv[4])
      if len(argv) > 5:
        stop_at = int(argv[5])

  print("READING FILES FROM: " + supplied_path)
  file_read = file_reader.FileReader(binfile, supplied_path)
  binarr = file_read.read_file()
  opcode_map = opcodes.opcode_tuples

  print("DISASSEMBLING MACHINE CODE...")
  reading = machine_code_reader.MachineCodeReader(opcode_map, offset, stop_at)
  lines = reading.disassemble(binarr)

  file_write = file_writer.FileWriter(asmfile, supplied_path)
  file_write.write(lines)


