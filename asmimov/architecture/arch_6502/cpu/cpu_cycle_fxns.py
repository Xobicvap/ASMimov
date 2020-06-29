from .cpu_state_operations import *

# none of these have the operations defined, for now they just define the cycle
# operations needed
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

  # php
  0x08: [
    read_next_and_throw_away,
    php
  ],

  # ora #$xx
  0x09: [

  ],

  # asl a
  0x0a: [
    Implied(asl)
  ],

  # jsr
  0x20: [
    fetch_value_and_increment_pc,
    address_of_stack,
    push_pch_and_decrement_sp,
    push_pcl_and_decrement_sp,
    copy_lo_addr_to_pcl_and_fetch_hi_addr_to_pch
  ],

  # plp
  0x28: [
    read_next_and_throw_away,
    increment_sp,
    plp
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

  # pha
  0x48: [
    read_next_and_throw_away,
    pha
  ],

  # rts
  0x60: [
    read_next_and_throw_away,
    increment_sp,
    pull_pcl_and_increment_sp,
    pull_pch,
    increment_pc
  ],

  # pla
  0x68: [
    read_next_and_throw_away,
    increment_sp,
    pla
  ]
}