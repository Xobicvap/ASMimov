from .cpu_state_operations import *

per_cycle_fxns = {
  # brk
  0x00: [
    read_next_throw_away_inc_pc,
    push_pch_and_decrement_sp,
    push_pcl_and_decrement_sp,
    push_p_with_b_flag_and_decrement_sp,
    read_irq_vector_lo,
    read_irq_vector_hi
  ],

  # ora ($zp, x)
  0x01: [
    fetch_pointer_address_increment_pc,
    read_pointer_add_x,
    indexed_indirect_address_lo,
    indexed_indirect_address_hi,
    IndexedIndirectRead(ora)
  ],

  # ora $zp
  0x05: [
    fetch_address_zero_page_increment_pc,
    ZeroPageRead(ora)
  ],

  # asl $zp
  0x06: [
    fetch_address_zero_page_increment_pc,
    read_from_effective_address,
    ZeroPageReadModifyWrite(asl),
    write_new_to_effective_address
  ],

  # php
  0x08: [
    Implied(php)
  ],

  # ora #$xx
  0x09: [
    Immediate(ora)
  ],

  # asl a
  0x0a: [
    Implied(asl)
  ],

  # ora $nnnn
  0x0d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    AbsoluteRead(ora)
  ],

  # asl $nnnn
  0x0e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    read_from_effective_address,
    AbsoluteReadModifyWrite(asl),
    write_new_to_effective_address
  ],

  # bpl r
  0x10: [
    fetch_value_and_increment_pc,
    Relative(bpl),
    Relative(bpl)
  ],

  # ora ($nn), y
  0x11: [
    fetch_pointer_address_increment_pc,
    fetch_indirect_effective_address_lo,
    fetch_indirect_effective_address_hi_add_y,
    IndexedIndirectRead(ora),
    IndexedIndirectRead(ora)
  ],

  # ora $zp, x
  0x15: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    ZeroPageReadX(ora)
  ],

  # asl $zp, x
  0x16: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    read_from_effective_address,
    ZeroPageReadModifyWriteX(asl),
    write_new_to_effective_address
  ],

  # clc
  0x18: [
    Implied(clc)
  ],

  # ora $nnnn, y
  0x19: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_y_lo_increment_pc,
    AbsoluteReadY(ora),
    AbsoluteReadY(ora)
  ],

  # ora $nnnn, x
  0x1d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    AbsoluteReadX(ora),
    AbsoluteReadX(ora)
  ],

  # asl $nnnn, x
  0x1e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    read_from_effective_fix_address,
    read_from_effective_address,
    AbsoluteReadModifyWriteX(asl),
    write_new_to_effective_address
  ],

  # jsr
  0x20: [
    fetch_value_and_increment_pc,
    address_of_stack,
    push_pch_and_decrement_sp,
    push_pcl_and_decrement_sp,
    copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch
  ],

  # and ($zp, x)
  0x21: [
    fetch_pointer_address_increment_pc,
    read_pointer_add_x,
    indexed_indirect_address_lo,
    indexed_indirect_address_hi,
    IndexedIndirectRead(logical_and)
  ],

  # bit $zp
  0x24: [
    fetch_address_zero_page_increment_pc,
    ZeroPageRead(bit_op)
  ],

  # and $zp
  0x25: [
    fetch_address_zero_page_increment_pc,
    ZeroPageRead(logical_and)
  ],

  # rol $zp
  0x26: [
    fetch_address_zero_page_increment_pc,
    read_from_effective_address,
    ZeroPageReadModifyWrite(rol),
    write_new_to_effective_address
  ],

  # plp
  0x28: [
    read_next_and_throw_away,
    increment_sp,
    plp
  ],

  # and #$xx
  0x29: [
    Immediate(logical_and)
  ],

  # rol
  0x2a: [
    Implied(rol)
  ],

  # bit $nnnn
  0x2c: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    AbsoluteRead(bit_op)
  ],

  # and $nnnn
  0x2d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    AbsoluteRead(logical_and)
  ],

  # rol $nnnn
  0x2e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    read_from_effective_address,
    AbsoluteReadModifyWrite(rol),
    write_new_to_effective_address
  ],

  # bmi r
  0x30: [
    fetch_value_and_increment_pc,
    Relative(bmi),
    Relative(bmi)
  ],

  # and ($zp), y
  0x31: [
    fetch_pointer_address_increment_pc,
    fetch_indirect_effective_address_lo,
    fetch_indirect_effective_address_hi_add_y,
    IndexedIndirectRead(logical_and),
    IndexedIndirectRead(logical_and)
  ],

  # ora $zp, x
  0x35: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    ZeroPageReadX(logical_and)
  ],

  # asl $zp, x
  0x36: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    read_from_effective_address,
    ZeroPageReadModifyWriteX(rol),
    write_new_to_effective_address
  ],

  # sec
  0x38: [
    Implied(sec)
  ],

  # and $nnnn, y
  0x39: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_y_lo_increment_pc,
    AbsoluteReadY(logical_and),
    AbsoluteReadY(logical_and)
  ],

  # and $nnnn, x
  0x3d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    AbsoluteReadX(logical_and),
    AbsoluteReadX(logical_and)
  ],

  # rol $nnnn, x
  0x3e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    read_from_effective_fix_address,
    read_from_effective_address,
    AbsoluteReadModifyWriteX(rol),
    write_new_to_effective_address
  ],

  # does this actually result in PC = BRK+2?
  # rti
  0x40: [
    read_next_and_throw_away,
    increment_sp,
    pull_p_and_increment_sp,
    pull_pcl_and_increment_sp,
    pull_pch
  ],

  # ora ($zp, x)
  0x01: [
    fetch_pointer_address_increment_pc,
    read_pointer_add_x,
    indexed_indirect_address_lo,
    indexed_indirect_address_hi,
    IndexedIndirectRead(ora)
  ],

  # eor $zp
  0x45: [
    fetch_address_zero_page_increment_pc,
    ZeroPageRead(eor)
  ],

  # lsr $zp
  0x46: [
    fetch_address_zero_page_increment_pc,
    read_from_effective_address,
    ZeroPageReadModifyWrite(lsr),
    write_new_to_effective_address
  ],

  # pha
  0x48: [
    read_next_and_throw_away,
    pha
  ],

  # eor #$xx
  0x49: [
    Immediate(eor)
  ],

  # lsr a
  0x4a: [
    Implied(lsr)
  ],

  # jmp $nnnn
  0x4c: [
    fetch_value_and_increment_pc,
    copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch
  ],

  # eor $nnnn
  0x4d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    AbsoluteRead(eor)
  ],

  # lsr $nnnn
  0x4e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    read_from_effective_address,
    AbsoluteReadModifyWrite(lsr),
    write_new_to_effective_address
  ],

  # bvc r
  0x50: [
    fetch_value_and_increment_pc,
    Relative(bvc),
    Relative(bvc)
  ],

  # eor ($nn), y
  0x51: [
    fetch_pointer_address_increment_pc,
    fetch_indirect_effective_address_lo,
    fetch_indirect_effective_address_hi_add_y,
    IndexedIndirectRead(eor),
    IndexedIndirectRead(eor)
  ],

  # eor $zp, x
  0x55: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    ZeroPageReadX(eor)
  ],

  # lsr $zp, x
  0x56: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    read_from_effective_address,
    ZeroPageReadModifyWriteX(lsr),
    write_new_to_effective_address
  ],

  # cli
  0x58: [
    Implied(cli)
  ],

  # eor $nnnn, y
  0x59: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_y_lo_increment_pc,
    AbsoluteReadY(eor),
    AbsoluteReadY(eor)
  ],

  # eor $nnnn, x
  0x5d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    AbsoluteReadX(eor),
    AbsoluteReadX(eor)
  ],

  # lsr $nnnn, x
  0x5e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    read_from_effective_fix_address,
    read_from_effective_address,
    AbsoluteReadModifyWriteX(lsr),
    write_new_to_effective_address
  ],

  # rts
  0x60: [
    read_next_and_throw_away,
    increment_sp,
    pull_pcl_and_increment_sp,
    pull_pch,
    increment_pc
  ],

  # adc ($zp), y
  0x61: [
    fetch_pointer_address_increment_pc,
    fetch_indirect_effective_address_lo,
    fetch_indirect_effective_address_hi_add_y,
    IndexedIndirectRead(adc),
    IndexedIndirectRead(adc)
  ],

  # adc $zp
  0x65: [
    fetch_address_zero_page_increment_pc,
    ZeroPageRead(adc)
  ],

  # ror $zp
  0x66: [
    fetch_address_zero_page_increment_pc,
    read_from_effective_address,
    ZeroPageReadModifyWrite(ror),
    write_new_to_effective_address
  ],

  # pla
  0x68: [
    read_next_and_throw_away,
    increment_sp,
    pla
  ],

  # adc #$xx
  0x69: [
    Immediate(adc)
  ],

  # lsr a
  0x6a: [
    Implied(ror)
  ],

  # adc $nnnn
  0x6d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    AbsoluteRead(adc)
  ],

  # ror $nnnn
  0x6e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    read_from_effective_address,
    AbsoluteReadModifyWrite(ror),
    write_new_to_effective_address
  ],

  # bvs r
  0x70: [
    fetch_value_and_increment_pc,
    Relative(bvs),
    Relative(bvs)
  ],

  # adc ($nn), y
  0x71: [
    fetch_pointer_address_increment_pc,
    fetch_indirect_effective_address_lo,
    fetch_indirect_effective_address_hi_add_y,
    IndexedIndirectRead(adc),
    IndexedIndirectRead(adc)
  ],

  # adc $zp, x
  0x75: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    ZeroPageReadX(adc)
  ],

  # ror $zp, x
  0x76: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    read_from_effective_address,
    ZeroPageReadModifyWriteX(ror),
    write_new_to_effective_address
  ],

  # sei
  0x78: [
    Implied(sei)
  ],

  # adc $nnnn, y
  0x79: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_y_lo_increment_pc,
    AbsoluteReadY(adc),
    AbsoluteReadY(adc)
  ],

  # adc $nnnn, x
  0x7d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    AbsoluteReadX(adc),
    AbsoluteReadX(adc)
  ],

  # ror $nnnn, x
  0x7e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    read_from_effective_fix_address,
    read_from_effective_address,
    AbsoluteReadModifyWriteX(ror),
    write_new_to_effective_address
  ],

  # sta ($zp, x)
  0x81: [
    fetch_pointer_address_increment_pc,
    read_pointer_add_x,
    indexed_indirect_address_lo,
    indexed_indirect_address_hi,
    WriteRegisterOperation(sta)
  ],

  # sty $zp
  0x84: [
    fetch_address_zero_page_increment_pc,
    WriteRegisterOperation(sty)
  ],

  # sta $zp
  0x85: [
    fetch_address_zero_page_increment_pc,
    WriteRegisterOperation(sta)
  ],

  # stx $zp
  0x86: [
    fetch_address_zero_page_increment_pc,
    WriteRegisterOperation(stx)
  ],

  # dey
  0x88: [
    Implied(dey)
  ],

  # txa
  0x8a: [
    Implied(txa)
  ],

  # sty $nnnn
  0x8c: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    WriteRegisterOperation(sty)
  ],

  # sta $nnnn
  0x8d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    WriteRegisterOperation(sta)
  ],

  # stx $nnnn
  0x8e: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_increment_pc,
    WriteRegisterOperation(stx)
  ],

  # bcc r
  0x90: [
    fetch_value_and_increment_pc,
    Relative(bcc),
    Relative(bcc)
  ],

  # sta ($zp), y
  0x91: [
    fetch_pointer_address_increment_pc,
    fetch_indirect_effective_address_lo,
    fetch_indirect_effective_address_hi_add_y,
    IndirectIndexedWrite(sta),
    WriteRegisterOperation(sta)
  ],

  # sty $zp, x
  0x94: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    WriteRegisterOperation(sty)
  ],

  # sty $zp, x
  0x95: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_x,
    WriteRegisterOperation(sta)
  ],

  # stx $zp, y
  0x96: [
    fetch_address_zero_page_increment_pc,
    read_effective_add_y,
    WriteRegisterOperation(stx)
  ],

  # tya
  0x98: [
    Implied(tya)
  ],

  # sta $nnnn, y
  0x99: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_y_lo_increment_pc,
    AbsoluteReadY(sta),
    WriteRegisterOperation(sta)
  ],

  # txs
  0x9a: [
    Implied(txs)
  ],

  # sta $nnnn, x
  0x9d: [
    fetch_address_lo_byte_increment_pc,
    fetch_address_hi_byte_add_x_lo_increment_pc,
    AbsoluteReadX(sta),
    WriteRegisterOperation(sta)
  ],

  # bcs r
  0xb0: [
    fetch_value_and_increment_pc,
    Relative(bcs),
    Relative(bcs)
  ],

  # bne r
  0xd0: [
    fetch_value_and_increment_pc,
    Relative(bne),
    Relative(bne)
  ],

  # beq r
  0xf0: [
    fetch_value_and_increment_pc,
    Relative(beq),
    Relative(beq)
  ]
}