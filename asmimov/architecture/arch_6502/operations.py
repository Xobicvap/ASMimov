#############################
# NO OPERATION
#############################

def nop(system, instruction):
  return {}

#############################
# SHIFT / ROTATE
############################

def rol(system, instruction):
  l, carry, dest = instruction.metadata()
  bit7 = l & 0x80
  x = (l << 1) & 0xff
  # is the carry _replaced_ here, or is it compared with the new value?
  x = x + 1 if carry == 1 else x
  c = 1 if bit7 != 0 else 0
  n = compute_n(x)
  z = compute_z(x)

  return {
    dest: x,
    "P": {"N": n, "Z": z, "C": c}
  }

def ror(system, instruction):
  l, carry, dest = instruction.metadata()
  bit0 = l & 0x01
  # i _think_ for this and lsr this is sufficient, and no stray upper bits
  # will come in
  x = l >> 1

  x = x + 0x80 if carry == 1 else x
  c = 1 if bit0 != 0 else 0
  n = compute_n(x)
  z = compute_z(x)

  return {
    dest: x,
    "P": {"N": n, "Z": z, "C": c}
  }

def asl(system, instruction):
  l, r, dest = instruction.metadata()
  bit7 = l & 0x80
  x = (l << 1) & 0xff
  c = 1 if bit7 != 0 else 0
  z = compute_z(x)
  n = compute_n(x)
  
  return {
    dest: x,
    "P": {"N": n, "Z": z, "C": c}
  }

def lsr(system, instruction):
  l, r, dest = instruction.metadata()
  bit0 = l & 0x01
  x = l >> 1
  c = 1 if bit0 != 0 else 0
  z = compute_z(x)
  n = compute_n(x)
  return {
    dest: x,
    "P": {"N": n, "Z": z, "C": c}
  }



#################################
# ADDITION / SUBTRACTION / COMPARISON
#################################

def adc(system, instruction):
  l, r, dest = instruction.metadata()
  carry = system.status("C")
  decimal = system.status("D")
  if decimal == 1:
    l_lo = l & 0xf
    l_hi = (l & 0xf0) >> 4
    r_lo = r & 0xf
    r_hi = (r & 0xf0) >> 4

    lo_nib = l_lo + r_lo + carry
    hi_nib = l_hi + r_hi

    #print("LO: " + str(lo_nib))
    #print("HI: " + str(hi_nib))

    if lo_nib > 9:
      hi_nib = hi_nib + 1
      lo_nib = lo_nib - 10

    hi_dec = hi_nib * 10
    temp = hi_dec + lo_nib

    #print("TEMP: " + str(temp))

    c = 1 if temp > 99 else 0
    if c == 1:
      temp = temp - 100

    xstr = "0x" + str(temp)
    x = int(xstr, 16)

  else:
    x = l + r + carry
    c = 1 if x > 0xff else 0
    x = x & 0xff

  # n and z are valid in that they at least match the accumulator value
  z = 1 if x == 0 and c == 0 else 0
  n = compute_n(x)

  # this is basically a crapshoot in decimal mode
  v = compute_v(x, r, l)
  
  return {
    dest: x,
    "P": {"N": n, "Z": z, "V": v, "C": c}
  }

def sbc(system, instruction):
  l, r, dest = instruction.metadata()
  carry = system.status("C")
  decimal = system.status("D")
  x = l - r - carry

  n = compute_n(x)
  z = compute_z(x)
  v = compute_v(x, r, l)

  if decimal == 1:
    temp1 = l & 0x0f
    temp2 = r & 0x0f
    temp3 = temp1 - carry 
    x = x - 6 if temp3 < temp2 else x
    if x > 0x99:
      x = x - 0x60

  c = 1 if x > 0xff else 0
  x = x & 0xff
  return {
    dest: x,
    "P": {"N": n, "Z": z, "V": v, "C": c}
  }

def cmp8(system, instruction):
  return compare(system, instruction)

def cpx(system, instruction):
  return compare(system, instruction)

def cpy(system, instruction):
  return compare(system, instruction)


##########################
# TRANSFER / INCREMENT / DECREMENT
##########################

def dey(system, instruction):
  return decrement(system, instruction)

def dex(system, instruction):
  return decrement(system, instruction)

def tax(system, instruction):
  return transfer(system, instruction)

def tay(system, instruction):
  return transfer(system, instruction)

def txa(system, instruction):
  return transfer(system, instruction)

def tya(system, instruction):
  return transfer(system, instruction)

def txs(system, instruction):
  l, r, dest = instruction.metadata()
  return { dest: l }

def tsx(system, instruction):
  return transfer(system, instruction)

def inx(system, instruction):
  return increment(system, instruction)

def iny(system, instruction):
  return increment(system, instruction)



##########################
# LOAD / STORE MEMORY
##########################

def sta(system, instruction):
  return move(system, instruction)

def sty(system, instruction):
  return move(system, instruction)

def stx(system, instruction):
  return move(system, instruction)

def lda(system, instruction):
  return move(system, instruction, True)

def ldy(system, instruction):
  return move(system, instruction, True)

def ldx(system, instruction):
  return move(system, instruction, True)



##########################
# SET / CLEAR INSTRUCTIONS
##########################

def clc(system, instruction):
  return {"P": {"C": 0}}

def sec(system, instruction):
  return {"P": {"C": 1}}

def cli(system, instruction):
  return {"P": {"I": 0}}

def sei(system, instruction):
  return {"P": {"I": 1}}



##########################
# PUSH / POP
##########################

def php(system, instruction): 
  l, r, dest = instruction.metadata()

  return {
    "push": l
  }

def plp(system, instruction):
  l, r, dest = instruction.metadata()

  return {
    dest: l,
    "pop": 1
  }

def pha(system, instruction):
  l, r, dest = instruction.metadata()

  return {
    "push": l
  }

def pla(system, instruction):
  l, r, dest = instruction.metadata()

  return {
    dest: l,
    "pop": 1
  }


#################################
# JUMPS, BRANCHES, RETURNS
#################################

# these could be simplified further into result_clear() vs result_set()
def bmi(system, instruction):
  metadata = instruction.metadata()
  r = metadata[1]
  return branch(r == 1, system, metadata)

def bpl(system, instruction): 
  metadata = instruction.metadata()
  r = metadata[1]
  return branch(r == 0, system, metadata)

def bvc(system, instruction):
  metadata = instruction.metadata()
  r = metadata[1]
  return branch(r == 0, system, metadata)

def bvs(system, instruction):
  metadata = instruction.metadata()
  r = metadata[1]
  return branch(r == 1, system, metadata)

def bcc(system, instruction):
  metadata = instruction.metadata()
  r = metadata[1]
  return branch(r == 0, system, metadata)

def bcs(system, instruction):
  metadata = instruction.metadata()
  r = metadata[1],
  return branch(r == 1, system, metadata)

def jsr(system, instruction):
  jump_dest, pc, dest = instruction.metadata()

  # the -1 here, though redundant, is just to show what it's _doing_
  pc = (pc + 3) - 1
  
  pc_lo, pc_hi = break_16bit_addr(pc)

  return {
    "push": [pc_hi, pc_lo], 
    dest: l
  }

def rti(system, instruction):
  l, r, dest = instruction.metadata()
  return {
    dest: l,
    "pop": 2
  }

def rts(system, instruction):
  l, r, dest = instruction.metadata()
  return {
    dest: l + 1,
    "pop": 2
  }

###################################
# BITWISE LOGICAL OPERATORS
###################################

def logical_and(system, instruction):
  l, r, dest = instruction.metadata()
  x = l & r
  z = compute_z(x)
  n = compute_n(x)
  return {
    dest: x, 
    "P": {"N": n, "Z": z}
  }

def ora(system, instruction):
  l, r, dest = instruction.metadata()  
  x = l | r
  z = compute_z(x)
  n = compute_n(x)
  
  return {
    dest: x,
    "P": {"N": n, "Z": z}
  }

def eor(system, instruction):
  l, r, dest = instruction.metadata()
  x = l ^ r
  z = compute_z(x)
  n = compute_n(x)
  return {
    dest: x,
    "P": {"N": n, "Z": z}
  }

def bit(system, instruction):
  l, r, dest = instruction.metadata()
  bit6 = 1 if r & 0x40 != 0 else 0
  bit7 = 1 if r & 0x80 != 0 else 0
  z = 1 if l & r == 0 else 0
  return {
    "P": {"N": bit7, "V": bit6, "Z": z}
  }


##############################
# INTERNAL FUNCTIONS
##############################

def twos_complement(n):
  return (0xff - n) + 1

def sign_branch_offset(branch_disp):
  if branch_disp < 0x80:
    return branch_disp
  return -twos_complement(branch_disp)

def break_16bit_addr(operand):
  addr_hi = (operand & 0xff00) >> 8
  addr_lo = operand & 0xff
  return (addr_lo, addr_hi)

def compute_n(x):
  return 1 if x & 0x80 != 0 else 0

def compute_z(x):
  return 1 if x==0 else 0

def compute_v(x, src, a):
  # again, this may be completely wrong
  temp1 = (a | x) & (src | x) & 0x80
  temp2 = 1 if temp1 & 0x80 == 0x80 else 0
  return temp2

def move(system, instruction, load=False):
  l, r, dest = instruction.metadata()
  
  if load:
    z = compute_z(l)
    n = compute_n(l)

    return {
      dest: l,
      "P": {"Z": z, "N": n}
    }

  return {
    dest: l
  }

def increment(system, instruction):
  l, r, dest = instruction.metadata()
  l = l + 1
  if l > 0xff:
    l = 0
  return t_inc_dec_base(l, dest)

def decrement(system, instruction):
  l, r, dest = instruction.metadata()
  l = l - 1
  if l < 0:
    l = 0xff
  return t_inc_dec_base(l, dest)

def transfer(system, instruction):
  l, r, dest = instruction.metadata()
  return t_inc_dec_base(l, dest)

def t_inc_dec_base(result, dest):
  z = compute_z(result)
  n = compute_n(result)

  return {
    dest: result,
    "P": {"Z": z, "N": n}
  }

def compare(system, instruction):
  l, r, dest = instruction.metadata()

  # not sure if this is correct for decimal mode
  x = l - r
  c = 1 if l >= r else 0
  n = compute_n(x)
  z = 1 if l == r else 0

  return {
    "P": {"N": n, "Z": z, "C": c}
  }

def get_decimal_parts(l, r):
  l_lo = l & 0xf
  l_hi = (l & 0xf0) >> 4
  r_lo = r & 0xf
  r_hi = (r & 0xf0) >> 4

  return (l_lo, l_hi, r_lo, r_hi)


def branch(will_branch, system, instruction):
  l, r, dest = instruction.metadata()
  branch_offset = l
  after_instruction = pc + pc_disp
  if will_branch:
    branch_offset = sign_branch_offset(branch_offset)
    
    # increment cycles used if branch is taken
    cycles = cycles + 1

    branch_disp = pc + branch_offset

    after_instruction_page = after_instruction & 0xff00
    after_branch_disp_page = branch_disp & 0xff00
    if after_branch_disp_page != after_instruction_page:
      cycles = cycles + 1
    return {"PC": branch_offset, "cycles": cycles}
  return {"PC": after_instruction, "cycles": cycles}
