from .cpu_states import *

def compute_bit7_set(v):
  return 1 if v.bit_set(7) else 0

def compute_z(v):
  return 1 if v == 0 else 0

def php(cpu):
  return push_register_decrement_sp(cpu, "P")

def pha(cpu):
  return push_register_decrement_sp(cpu, "A")

def pla(cpu):
  return pull_register(cpu, "A")

def plp(cpu):
  return pull_register(cpu, "P")

def asl(cpu, v=None):
  is_implied = False
  if v is None:
    v = cpu.a()
    is_implied = True
  c = compute_bit7_set(v)
  v = v << 1


class Implied:
  def __init__(self, operation):
    self.operation = operation

  def __call__(self, cpu):
    read_next_and_throw_away(cpu)
    return self.operation(cpu)







