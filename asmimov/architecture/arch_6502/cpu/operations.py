#############################
# NO OPERATION
#############################

def nop(cpu_container, instruction):
  return {}


#############################
# SHIFT / ROTATE
############################

def rol(cpu_container, instruction):
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

def ror(cpu_container, instruction):
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

def asl(cpu_container, instruction):
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

def lsr(cpu_container, instruction):
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

def adc(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  carry = cpu_container.status("C")
  decimal = cpu_container.status("D")
  if decimal == 1:
    l_lo, l_hi, r_lo, r_hi = get_decimal_parts(l, r)

    lo_nib = l_lo + r_lo + carry
    hi_nib = l_hi + r_hi

    if lo_nib > 9:
      hi_nib = hi_nib + 1
      lo_nib = lo_nib - 10

    hi_dec = hi_nib * 10
    temp = hi_dec + lo_nib

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

def sbc(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  carry = 1 if cpu_container.status("C") == 0 else 0
  decimal = cpu_container.status("D")

  if decimal == 1:
    l_lo, l_hi, r_lo, r_hi = get_decimal_parts(l, r)

    # carry logic may be wrong below
    if l_lo < r_lo:
      l_lo = l_lo + 10
      l_hi = l_hi - 1

    lo_nib = l_lo - r_lo
    hi_nib = l_hi - r_hi

    hi_dec = hi_nib * 10
    temp = hi_dec + lo_nib if hi_dec > 0 else hi_dec - lo_nib

    c = 0 if temp < 0 else 1
    if c == 0:
      temp = 100 + temp

    xstr = "0x" + str(temp)
    x = int(xstr, 16)

  else:
    x = l - r - carry
    c = 0 if x < 0 else 1
    x = x & 0xff # this may be wrong

  # n and z are valid in that they at least match the accumulator value
  z = 1 if x == 0 and c == 0 else 0
  n = compute_n(x)

  # this is basically a crapshoot in decimal mode
  v = compute_v(x, r, l)
  
  return {
    dest: x,
    "P": {"N": n, "Z": z, "V": v, "C": c}
  }

def cmp8(cpu_container, instruction):
  return compare(cpu_container, instruction)

def cpx(cpu_container, instruction):
  return compare(cpu_container, instruction)

def cpy(cpu_container, instruction):
  return compare(cpu_container, instruction)


##########################
# TRANSFER / INCREMENT / DECREMENT
##########################

def dey(cpu_container, instruction):
  return decrement(cpu_container, instruction)

def dex(cpu_container, instruction):
  return decrement(cpu_container, instruction)

def dec(cpu_container, instruction):
  return decrement(cpu_container, instruction)

def tax(cpu_container, instruction):
  return transfer(cpu_container, instruction)

def tay(cpu_container, instruction):
  return transfer(cpu_container, instruction)

def txa(cpu_container, instruction):
  return transfer(cpu_container, instruction)

def tya(cpu_container, instruction):
  return transfer(cpu_container, instruction)

def txs(cpu_container, instruction):
  return xfer_stack_pointer(cpu_container, instruction)

def tsx(cpu_container, instruction):
  return xfer_stack_pointer(cpu_container, instruction)

def inx(cpu_container, instruction):
  return increment(cpu_container, instruction)

def iny(cpu_container, instruction):
  return increment(cpu_container, instruction)

def inc(cpu_container, instruction):
  return increment(cpu_container, instruction)


##########################
# LOAD / STORE MEMORY
##########################

def sta(cpu_container, instruction):
  return move(cpu_container, instruction)

def sty(cpu_container, instruction):
  return move(cpu_container, instruction)

def stx(cpu_container, instruction):
  return move(cpu_container, instruction)

def lda(cpu_container, instruction):
  return move(cpu_container, instruction, True)

def ldy(cpu_container, instruction):
  return move(cpu_container, instruction, True)

def ldx(cpu_container, instruction):
  return move(cpu_container, instruction, True)


##########################
# SET / CLEAR INSTRUCTIONS
##########################

def clc(cpu_container, instruction):
  return {"P": {"C": 0}}

def sec(cpu_container, instruction):
  return {"P": {"C": 1}}

def cli(cpu_container, instruction):
  return {"P": {"I": 0}}

def sei(cpu_container, instruction):
  return {"P": {"I": 1}}

def cld(cpu_container, instruction):
  return {"P": {"D": 0}}

def sed(cpu_container, instruction):
  return {"P": {"D": 1}}

def clv(cpu_container, instruction):
  return {"P": {"V": 0}}


##########################
# PUSH / POP
##########################

def php(cpu_container, instruction): 
  status, _, _ = instruction.metadata()

  status = status | 0x30  # 00110000
  stack_ptr = cpu_container.cpu_register("SP")

  return {
    "SP": stack_ptr - 1,
    stack_ptr + 0x100: status
  }

def plp(cpu_container, instruction):
  status, _, dest = instruction.metadata()
  status = status & 0xcf # 11001111

  stack_ptr = cpu_container.cpu_register("SP")
  
  # this way we set P to popped status register (minus nonexistent B flags)
  # and do the necessary stack pop
  return {
    dest: status,
    "SP": stack_ptr + 1
  }

def pha(cpu_container, instruction):
  a, _, _ = instruction.metadata()
  stack_ptr = cpu_container.cpu_register("SP")

  return {
    "SP": stack_ptr - 1,
    stack_ptr + 0x100: a
  }

def pla(cpu_container, instruction):
  a, _, dest = instruction.metadata()
  stack_ptr = cpu_container.cpu_register("SP")

  return {
    dest: a,
    "SP": stack_ptr + 1
  }


#################################
# JUMPS, BRANCHES, RETURNS
#################################

# these could be simplified further into result_clear() vs result_set()
def bmi(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 1, cpu_container, instruction)

def bpl(cpu_container, instruction): 
  r = instruction.metadata()[1]
  return branch(r == 0, cpu_container, instruction)

def bvc(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 0, cpu_container, instruction)

def bvs(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 1, cpu_container, instruction)

def bcc(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 0, cpu_container, instruction)

def bcs(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 1, cpu_container, instruction)

def bne(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 0, cpu_container, instruction)

def beq(cpu_container, instruction):
  r = instruction.metadata()[1]
  return branch(r == 1, cpu_container, instruction)

def jsr(cpu_container, instruction):
  jump_dest, pc, dest = instruction.metadata()

  # the -1 here, though redundant, is just to show what it's _doing_
  pc = (pc + 3) - 1
  
  pc_lo, pc_hi = break_16bit_addr(pc)
  stack_ptr = cpu_container.cpu_register("SP")
  stack_ptr_addr = stack_ptr + 0x100

  return {
    # make sure the order here is correct such that the stack looks like:
    # PC_LO, PC_HI
    stack_ptr_addr: pc_hi,
    stack_ptr_addr - 1: pc_lo,
    stack_ptr: stack_ptr - 2,
    dest: jump_dest
  }

def jmp(cpu_container, instruction):
  jump_dest, _, dest = instruction.metadata()

  return {
    dest: jump_dest
  }

def brk(cpu_container, instruction):
  # "the program bank register (PB, the A16-A23 part of the address bus)
  # is pushed onto the hardware stack" ... huh?

  status, pc, dest = instruction.metadata()
  
  pc = pc + 2
  pc_lo, pc_hi = break_16bit_addr(pc)

  status = status | 0x30 # 00110000, sets bits 5 and 4 in the copy for stack
  irq_vec = cpu_container.vector("IRQ/BRK")
  stack_ptr = cpu_container.cpu_register("SP")

  stack_ptr_addr = 0x100 + stack_ptr

  return {
    stack_ptr: stack_ptr - 3,
    dest: irq_vec,
    stack_ptr_addr: pc_hi,
    stack_ptr_addr - 1: pc_lo,
    stack_ptr_addr - 2: status
  }

def rti(cpu_container, instruction):
  # stack_ptr here is the actual pointer to stack
  stack_ptr, _, _ = instruction.metadata()

  # massage stack ptr to full 16-bit value
  # the made-up 'pop_byte' / 'pop_word' pseudo-addressing modes 
  # take care of this, but we have to manually do stack stuff for
  # this instruction
  stack_ptr = stack_ptr + 0x100 + 1
  
  status = cpu_container.read_direct(stack_ptr)
  status = status & 0xcf  # 11001111, ignore B flag

  stack_ptr = stack_ptr + 1
  pc = cpu_container.read_absolute_address(stack_ptr)

  return {
    "PC": pc,
    "P": status,
    stack_ptr: stack_ptr + 3
  }

def rts(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  stack_ptr = cpu_container.cpu_register("SP")

  return {
    dest: l + 1,
    "SP": stack_ptr + 2
  }

###################################
# BITWISE LOGICAL OPERATORS
###################################

def logical_and(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  x = l & r
  z = compute_z(x)
  n = compute_n(x)
  return {
    dest: x, 
    "P": {"N": n, "Z": z}
  }

def ora(cpu_container, instruction):
  l, r, dest = instruction.metadata()  
  x = l | r
  z = compute_z(x)
  n = compute_n(x)
  
  return {
    dest: x,
    "P": {"N": n, "Z": z}
  }

def eor(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  x = l ^ r
  z = compute_z(x)
  n = compute_n(x)
  return {
    dest: x,
    "P": {"N": n, "Z": z}
  }

def bit(cpu_container, instruction):
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

def move(cpu_container, instruction, load=False):
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

def increment(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  l = l + 1
  if l > 0xff:
    l = 0
  return t_inc_dec_base(l, dest)

def decrement(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  l = l - 1
  if l < 0:
    l = 0xff
  return t_inc_dec_base(l, dest)

def transfer(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  return t_inc_dec_base(l, dest)

def xfer_stack_pointer(cpu_container, instruction):
  l, r, dest = instruction.metadata()
  return { dest: l }

def t_inc_dec_base(result, dest):
  z = compute_z(result)
  n = compute_n(result)

  return {
    dest: result,
    "P": {"Z": z, "N": n}
  }

def compare(cpu_container, instruction):
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

def branch(will_branch, cpu_container, instruction):
  l, r, pc = instruction.metadata()
  pc_disp, cycles = instruction.pc_metadata()
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
    return {"PC": branch_disp, "cycles": cycles}
  return {"PC": after_instruction, "cycles": cycles}
