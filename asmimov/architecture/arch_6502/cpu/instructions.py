from addressing_modes import *
from operations import *

# tuple structure
# (
#   change function,
#   memory addressing type,
#   operand1,
#   operand2,
#   destination,
#   memory_operand,
#   PC displacement,
#   cycles
# )

instruction_tuples = {
  # how do we set this?
  0x00: (
    brk,
    None,
    "P",
    "PC",
    "PC",
    2,
    7
  ),
  0x01: (
    ora,
    indexed_indirect,
    "A",
    "operand",
    "A",
    2,
    6
  ),
  0x05: (
    ora,
    zero_page,
    "A",
    "operand",
    "A",
    2,
    3
  ),
  0x06: (
    asl,
    zero_page,
    "operand",
    None,
    "operand",
    2,
    5
  ),
  0x08: (
    php,
    None,
    "P",
    None,
    "push",
    1,
    3
  ),
  0x09: (
    ora,
    immediate,
    "A",
    "operand",
    "A",
    1,
    2
  ),
  0x0a: (
    asl,
    immediate,
    "A",
    None,
    "A",
    1,
    2
  ),
  0x0d: (
    ora,
    absolute,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x0e: (
    asl,
    absolute,
    "operand",
    None,
    "operand",
    3,
    4
  ),
  0x10: (
    bpl,
    branch_offset,
    "operand",
    "N",
    "PC",
    2,
    2
  ),
  0x11: (
    ora,
    indirect_indexed,
    "A",
    "operand",
    "A",
    2,
    5
  ),
  0x15: (
    ora,
    zero_page_x,
    "A",
    "operand",
    "A",
    2,
    4
  ),
  0x16: (
    asl,
    zero_page_x,
    "operand",
    None,
    "operand",
    2,
    6
  ),
  0x18: (
    clc,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0x19: (
    ora,
    absolute_y,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x1d: (
    ora,
    absolute_x,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x1e: (
    asl,
    absolute_x,
    "operand",
    None,
    "operand",
    3,
    7
  ),
  0x20: (
    jsr,
    absolute,
    "operand",
    "PC",
    "PC",
    3,
    6
  ),
  0x21: (
    logical_and,
    indexed_indirect,
    "A",
    "operand",
    "A",
    2,
    6
  ),
  0x24: (
    bit,
    zero_page,
    "A",
    "operand",
    "P",
    2,
    3
  ),
  0x25: (
    logical_and,
    zero_page,
    "A",
    "operand",
    "A",
    2,
    3
  ),
  0x26: (
    rol,
    zero_page,
    "operand",
    "C",
    "operand",
    2,
    5
  ),
  0x28: (
    plp,
    pop_byte,
    "SP",
    None,
    "P",
    1,
    4
  ),
  0x29: (
    logical_and,
    immediate,
    "A",
    "operand",
    "A",
    2,
    2
  ),
  0x2a: (
    rol,
    immediate,
    "A",
    None,
    "A",
    1,
    2
  ),
  0x2c: (
    bit,
    absolute,
    "A",
    "operand",
    "P",
    3,
    4
  ),
  0x2d: (
    logical_and,
    absolute,
    "A",
    "operand",
    "A",
    3,
    4,
  ),
  0x2e: (
    rol,
    immediate,
    "A",
    None,
    "A",
    1,
    2
  ),
  0x30: (
    bmi,
    relative,
    "operand",
    "N",
    "PC",
    2,
    2
  ),
  0x31: (
    logical_and,
    indirect_indexed,
    "A",
    "operand",
    "A",
    2,
    5
  ),
  0x35: (
    logical_and,
    zero_page_x,
    "A",
    "operand",
    "A",
    2,
    4
  ),
  0x36: (
    rol,
    zero_page_x,
    "operand",
    "C",
    "operand",
    2,
    6
  ),
  0x38: (
    sec,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0x39: (
    logical_and,
    absolute_y,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x3d: (
    logical_and,
    absolute_x,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x3e: (
    rol,
    absolute_x,
    "operand",
    "C",
    "operand",
    3,
    7
  ),
  0x40: (
    rti,
    None,
    "SP",
    None,
    # it's not _really_ none, but it sets two things at once 
    # which doesn't have a paradigm
    None,
    1,
    6
  ),
  0x41: (
    eor,
    indexed_indirect,
    "A",
    "operand",
    "A",
    2,
    6
  ),
  0x45: (
    eor,
    zero_page,
    "A",
    "operand",
    "A",
    2,
    3
  ),
  0x46: (
    lsr,
    zero_page,
    "operand",
    None,
    "operand",
    2,
    5
  ),
  0x48: (
    pha,
    None,
    "A",
    None,
    "push",
    1,
    3
  ),
  0x49: (
    eor,
    immediate,
    "A",
    "operand",
    "A",
    2,
    2
  ),
  0x4a: (
    lsr,
    immediate,
    "A",
    None,
    "A",
    1,
    2
  ),
  0x4c: (
    jmp,
    immediate,
    "operand",
    None,
    "PC",
    3,
    3
  ),
  0x4d: (
    eor,
    absolute,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x4e: (
    lsr,
    absolute,
    "operand",
    None,
    "operand",
    3,
    6
  ),
  0x50: (
    bvc,
    relative,
    "operand",
    "V",
    "PC",
    2,
    2
  ),
  0x51: (
    eor,
    indirect_indexed,
    "A",
    "operand",
    "A",
    2,
    5
  ),
  0x55: (
    eor,
    zero_page_x,
    "A",
    "operand",
    "A",
    2,
    4
  ),
  0x56: (
    lsr,
    zero_page_x,
    "operand",
    None,
    "operand",
    2,
    6
  ),
  0x58: (
    cli,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0x59: (
    eor,
    absolute_y,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x5d: (
    eor,
    absolute_x,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x60: (
    rts,
    pop_addr,
    "SP",
    None,
    "PC",
    1,
    6
  ),
  # is this right? should this add to A?
  0x61: (
    adc,
    indexed_indirect,
    "A",
    "operand",
    "A",
    2,
    6
  ),
  0x65: (
    adc,
    zero_page,
    "A",
    "operand",
    "A",
    2,
    3
  ),
  0x66: (
    ror,
    zero_page,
    "operand",
    "C",
    "operand",
    2,
    5
  ),
  0x68: (
    pla,
    pop_byte,
    "SP",
    None,
    "A",
    1,
    4
  ),
  0x69: (
    adc,
    immediate,
    "A",
    "operand",
    "A",
    2,
    2
  ),
  0x6a: (
    ror,
    immediate,
    "A",
    None,
    "A",
    1,
    2
  ),
  0x6c: (
    jmp,
    indirect,
    "operand",
    None,
    "PC",
    3,
    5
  ),
  0x6d: (
    adc,
    absolute,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x6e: (
    ror,
    absolute,
    "operand",
    "C",
    "operand",
    3,
    6
  ),
  0x70: (
    bvs,
    relative,
    "operand",
    "V",
    "PC",
    2,
    2
  ),
  0x71: (
    adc,
    indirect_indexed,
    "A",
    "operand",
    "A",
    2,
    5
  ),
  0x75: (
    adc,
    zero_page_x,
    "A",
    "operand",
    "A",
    2,
    4
  ),
  0x76: (
    ror,
    zero_page_x,
    "operand",
    "C",
    "operand",
    2,
    6
  ),
  0x78: (
    sei,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0x79: (
    adc,
    absolute_y,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x7d: (
    adc,
    absolute_x,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0x7e: (
    ror,
    absolute_x,
    "operand",
    "C",
    "operand",
    3,
    7
  ),
  0x81: (
    sta,
    indexed_indirect,
    "A",
    None,
    "operand",
    2,
    6
  ),
  0x84: (
    sty,
    zero_page,
    "Y",
    None,
    "operand",
    2,
    3
  ),
  0x85: (
    sta,
    zero_page,
    "A",
    None,
    "operand",
    2,
    3
  ),
  0x86: (
    stx,
    zero_page,
    "X",
    None,
    "operand",
    2,
    3
  ),
  0x88: (
    dey,
    immediate, # really implied, but w/e
    "Y",
    None,
    "Y",
    1,
    2
  ),
  0x8a: (
    txa,
    immediate, # see dey
    "X",
    None,
    "A",
    1,
    2
  ),
  0x8c: (
    sty,
    absolute,
    "Y",
    None,
    "operand",
    3,
    4
  ),
  0x8d: (
    sta,
    absolute,
    "A",
    None,
    "operand",
    3,
    4
  ),
  0x8e: (
    stx,
    absolute,
    "X",
    None,
    "operand",
    3,
    4
  ),
  0x90: (
    bcc,
    relative,
    "operand",
    "C",
    "PC",
    2,
    2
  ),
  0x91: (
    sta,
    indirect_indexed,
    "A",
    None,
    "operand",
    2,
    6
  ),
  0x94: (
    sty,
    zero_page_x,
    "Y",
    None,
    "operand",
    2,
    4
  ),
  0x95: (
    sta,
    zero_page_x,
    "A",
    None,
    "operand",
    2,
    4
  ),
  0x96: (
    stx,
    zero_page_y,
    "X",
    None,
    "operand",
    2,
    4
  ),
  0x98: (
    tya,
    immediate,
    "Y",
    None,
    "A",
    1,
    2
  ),
  0x99: (
    sta,
    absolute_y,
    "A",
    None,
    "operand",
    3,
    5
  ),
  0x9a: (
    txs,
    immediate,
    "X",
    None,
    "SP",
    1,
    2
  ),
  0x9d: (
    sta,
    absolute_x,
    "A",
    None,
    "operand",
    3,
    5
  ),
  0xa0: (
    ldy,
    immediate,
    "operand",
    None,
    "Y",
    2,
    2
  ),
  0xa1: (
    lda,
    indexed_indirect,
    "operand",
    None,
    "A",
    2,
    6
  ),
  0xa2: (
    ldx,
    immediate,
    "operand",
    None,
    "X",
    2,
    2
  ),
  0xa4: (
    ldy,
    zero_page,
    "operand",
    None,
    "Y",
    2,
    3
  ),
  0xa5: (
    lda,
    zero_page,
    "operand",
    None,
    "A",
    2,
    3
  ),
  0xa6: (
    ldx,
    zero_page,
    "operand",
    None,
    "X",
    2,
    3
  ),
  0xa8: (
    tay,
    immediate,
    "A",
    None,
    "Y",
    1,
    2
  ),
  0xa9: (
    lda,
    immediate,
    "operand",
    None,
    "A",
    2,
    2
  ),
  0xaa: (
    tax,
    immediate,
    "A",
    None,
    "X",
    1,
    2
  ),
  0xac: (
    ldy,
    absolute,
    "operand",
    None,
    "Y",
    3,
    4
  ),
  0xad: (
    lda,
    absolute,
    "operand",
    None,
    "A",
    3,
    4
  ),
  0xae: (
    ldx,
    absolute,
    "operand",
    None,
    "X",
    3,
    4
  ),
  0xb0: (
    bcs,
    relative,
    "operand",
    "C",
    "PC",
    2,
    2
  ),
  0xb1: (
    lda,
    indirect_indexed,
    "operand",
    None,
    "A",
    2,
    5
  ),
  0xb4: (
    ldy,
    zero_page_x,
    "operand",
    None,
    "Y",
    2,
    4
  ),
  0xb5: (
    lda,
    zero_page_x,
    "operand",
    None,
    "A",
    2,
    4
  ),
  0xb6: (
    ldx,
    zero_page_y,
    "operand",
    None,
    "X",
    2,
    4
  ),
  0xb8: (
    clv,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0xb9: (
    lda,
    absolute_y,
    "operand",
    None,
    "A",
    3,
    4
  ),
  0xba: (
    tsx,
    immediate,
    "SP",
    None,
    "X",
    1,
    2
  ),
  0xbc: (
    ldy,
    absolute_x,
    "operand",
    None,
    "Y",
    3,
    4
  ),
  0xbd: (
    lda,
    absolute_x,
    "operand",
    None,
    "A",
    3,
    4
  ),
  0xbe: (
    ldx,
    absolute_y,
    "operand",
    None,
    "X",
    3,
    4
  ),
  0xc0: (
    cpy,
    immediate,
    "Y",
    "operand",
    None,
    2,
    2
  ),
  0xc1: (
    cmp8,
    indexed_indirect,
    "A",
    "operand",
    None,
    2,
    6
  ),
  0xc4: (
    cpy,
    zero_page,
    "Y",
    "operand",
    None,
    2,
    3
  ),
  0xc5: (
    cmp8,
    zero_page,
    "A",
    "operand",
    None,
    2,
    3
  ),
  0xc6: (
    dec,
    zero_page,
    "operand",
    None,
    "operand",
    2,
    5
  ),
  0xc8: (
    iny,
    immediate,
    "Y",
    None,
    "Y",
    1,
    2
  ),
  0xc9: (
    cmp8,
    immediate,
    "A",
    "operand",
    None,
    2,
    2
  ),
  0xca: (
    dex,
    immediate,
    "X",
    None,
    "X",
    1,
    2
  ),
  0xcc: (
    cpy,
    absolute,
    "Y",
    "operand",
    None,
    3,
    4
  ),
  0xcd: (
    cmp8,
    absolute,
    "A",
    "operand",
    None,
    3,
    4
  ),
  0xce: (
    dec,
    absolute,
    "operand",
    None,
    "operand",
    3,
    6
  ),
  0xd0: (
    bne,
    relative,
    "operand",
    "Z",
    "PC",
    2,
    2
  ),
  0xd1: (
    cmp8,
    indirect_indexed,
    "A",
    "operand",
    None,
    2,
    5
  ),
  0xd5: (
    cmp8,
    zero_page_x,
    "A",
    "operand",
    None,
    2,
    4
  ),
  0xd6: (
    dec,
    zero_page_x,
    "operand",
    None,
    "operand",
    2,
    6
  ),
  0xd8: (
    cld,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0xd9: (
    cmp8,
    absolute_y,
    "A",
    "operand",
    None,
    3,
    4
  ),
  0xdd: (
    cmp8,
    absolute_x,
    "A",
    "operand",
    None,
    3,
    4
  ),
  0xde: (
    dec,
    absolute_x,
    "operand",
    None,
    "operand",
    3,
    7
  ),
  0xe0: (
    cpx,
    immediate,
    "X",
    "operand",
    None,
    2,
    2
  ),
  0xe1: (
    sbc,
    indexed_indirect,
    "A",
    "operand",
    "A",
    2,
    6
  ),
  0xe4: (
    cpx,
    zero_page,
    "X",
    "operand",
    None,
    2,
    3
  ),
  0xe5: (
    sbc,
    zero_page,
    "A",
    "operand",
    "A",
    2,
    3
  ),
  0xe6: (
    inc,
    zero_page,
    "operand",
    None,
    "operand",
    2,
    5
  ),
  0xe8: (
    inx,
    immediate,
    "X",
    None,
    "X",
    1,
    2
  ),
  0xe9: (
    sbc,
    immediate,
    "A",
    "operand",
    "A",
    2,
    2
  ),
  0xea: (
    nop,
    immediate,
    None,
    None,
    None,
    1,
    2
  ),
  0xec: (
    cpx,
    absolute,
    "X",
    "operand",
    None,
    3,
    4
  ),
  0xed: (
    sbc,
    absolute,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0xee: (
    inc,
    absolute,
    "operand",
    None,
    "operand",
    3,
    6
  ),
  0xf0: (
    beq,
    relative,
    "operand",
    "Z",
    "PC",
    2,
    2
  ),
  0xf1: (
    sbc,
    indirect_indexed,
    "A",
    "operand",
    "A",
    2,
    5
  ),
  0xf5: (
    sbc,
    zero_page_x,
    "A",
    "operand",
    "A",
    2,
    4,
  ),
  0xf6: (
    inc,
    zero_page_x,
    "operand",
    None,
    "operand",
    2,
    6
  ),
  0xf8: (
    sed,
    None,
    "P",
    None,
    "P",
    1,
    2
  ),
  0xf9: (
    sbc,
    absolute_y,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0xfd: (
    sbc,
    absolute_x,
    "A",
    "operand",
    "A",
    3,
    4
  ),
  0xfe: (
    inc,
    absolute_x,
    "operand",
    None,
    "operand",
    3,
    7
  )
}
