from architecture.math.hexnum import ByteValue, WordValue


def setter(machine_state, flag, value):
  setattr(machine_state, flag, value)

def getter(machine_state, flag):
  return getattr(machine_state, flag)

def graphics_on(machine_state):
  setter(machine_state, "graphics", True)

def graphics_off(machine_state):
  setter(machine_state, "graphics", False)

def mixed_on(machine_state):
  setter(machine_state, "mixed", True)

def mixed_off(machine_state):
  setter(machine_state, "mixed", False)

def page1(machine_state):
  setter(machine_state, "page", True)

def page2(machine_state):
  setter(machine_state, "page", False)

def hires_on(machine_state):
  setter(machine_state, "hi_res", True)

def hires_off(machine_state):
  setter(machine_state, "hi_res", False)

def keyboard_data(machine_state):
  return ByteValue(getter(machine_state, "keyboard_data"))

def keyboard_strobe(machine_state):
  setter(machine_state, "keyboard_data",
         getter(machine_state, "keyboard_data") - 0x80)

def nothing(machine_state):
  pass

registers = [
  {
    "name": "TEXTOFF",
    "readfxn": graphics_on,
    "writefxn": graphics_on,
    "address": WordValue(0xc050)
  },
  {
    "name": "TEXTON",
    "readfxn": graphics_off,
    "writefxn": graphics_off,
    "address": WordValue(0xc051)
  },
  {
    "name": "MIXEDOFF",
    "readfxn": mixed_off,
    "writefxn": mixed_off,
    "address": WordValue(0xc052)
  },
  {
    "name": "MIXEDON",
    "readfxn": mixed_on,
    "writefxn": mixed_on,
    "address": WordValue(0xc053)
  },
  {
    "name": "MIXEDOFF",
    "readfxn": mixed_off,
    "writefxn": mixed_off,
    "address": WordValue(0xc052)
  }
]