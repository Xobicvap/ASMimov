from .operations import *

# 1. do we want read-write-modify instructions to be
# RWM? or more granular i.e. "read", "write", etc?
# 2.
instruction_map = {
  0x00: {
    "change_fxn": brk,
    "addressing": "brk",
    "pc_disp": 2,
    "cycles": 7,
    "left": "P",
    "right": "PC",
    "dest": "PC",
    "type": "program_flow",
    "name": "BRK",
    "opcode": 0x00,
  },
  0x01: {
    "change_fxn": ora,
    "addressing": "indexed indirect",
    "pc_disp": 2,
    "cycles": 6,
    "left": "A",
    "right": "operand1",
    "dest": "A",
    "type": "RWM",
    "name": "ORA",
    "opcode": 0x01
  },
  0x05: {
    "change_fxn": ora,
    "addressing": "zero page",
    "pc_disp": 2,
    "cycles": 3,
    "left": "A",
    "right": "operand1",
    "dest": "A",
    "type": "RWM",
    "name": "ORA",
    "opcode": 0x05
  },
  0x06: {
    "change_fxn": asl,
    "addressing": "zero page",
    "pc_disp": 2,
    "cycles": 5,
    "left": "addr_target",
    "right": None,
    "dest": "addr",
    "type": "RWM",
    "name": "ASL",
    "opcode": 0x06
  },
  0x08: {
    "change_fxn": php,
    "addressing": None,
    "pc_disp": 1,
    "cycles": 3,
    "left": None,
    "right": None,
    "dest": None,
    "type": "stack",
    "name": "PHP",
    "opcode": 0x08
  },
  0x09: {}

}
