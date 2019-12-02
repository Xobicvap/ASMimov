opcode_tuples = {
  0x00: ("BRK", 0, ""),
  0x01: ("ORA", 1, "($LL, X)"),
  0x05: ("ORA", 1, "$LL"),
  0x06: ("ASL", 1, "$LL"),
  0x08: ("PHP", 0, ""),
  0x09: ("ORA", 1, "#$BB"),
  0x0a: ("ASL", 0, "A"),
  0x0d: ("ORA", 2, "$HHLL"),
  0x0e: ("ASL", 2, "$HHLL"),
  0x10: ("BPL", 1, "$BB"),
  0x11: ("ORA", 1, "($LL), Y"),
  0x15: ("ORA", 1, "$LL, X"),
  0x16: ("ASL", 1, "$LL, X"),
  0x18: ("CLC", 0, ""),
  0x19: ("ORA", 2, "$HHLL, Y"),
  0x1d: ("ORA", 2, "$HHLL, X"),
  0x1e: ("ASL", 2, "$HHLL, X"),
  0x20: ("JSR", 2, "$HHLL"),
  0x21: ("AND", 1, "($LL, X)"),
  0x24: ("BIT", 1, "$LL"),
  0x25: ("AND", 1, "$LL"),
  0x26: ("ROL", 1, "$LL"),
  0x28: ("PLP", 0, ""),
  0x29: ("AND", 1, "$#BB"),
  0x2a: ("ROL", 0, "A"),
  0x2c: ("BIT", 2, "$HHLL"),
  0x2d: ("AND", 2, "$HHLL"),
  0x2e: ("ROL", 0, "A"),
  0x30: ("BMI", 1, "$BB"),
  0x31: ("AND", 1, "($LL), Y"),
  0x35: ("AND", 1, "$LL, X"),
  0x36: ("ROL", 1, "$LL, X"),
  0x38: ("SEC", 0, ""),
  0x39: ("AND", 2, "$HHLL, Y"),
  0x3d: ("AND", 2, "$HHLL, X"),
  0x3e: ("ROL", 2, "$HHLL, X"),
  0x40: ("RTI", 0, ""),
  0x41: ("EOR", 1, "($LL, X)"),
  0x45: ("EOR", 1, "$LL"),
  0x46: ("LSR", 1, "$LL"),
  0x48: ("PHA", 0, ""),
  0x49: ("EOR", 1, "#$BB"),
  0x4a: ("LSR", 0, "A"),
  0x4c: ("JMP", 2, "$HHLL"),
  0x4d: ("EOR", 2, "$HHLL"),
  0x4e: ("LSR", 2, "$HHLL"),
  0x50: ("BVC", 1, "$BB"),
  0x51: ("EOR", 1, "($LL), Y"),
  0x55: ("EOR", 1, "$LL, X"),
  0x56: ("LSR", 1, "$LL, X"),
  0x58: ("CLI", 0, ""),
  0x59: ("EOR", 2, "$HHLL, Y"),
  0x5d: ("EOR", 2, "$HHLL, X"),
  0x5e: ("LSR", 2, "$HHLL, X"),
  0x60: ("RTS", 0, ""),
  0x61: ("ADC", 1, "($LL, X)"),
  0x65: ("ADC", 1, "$LL"),
  0x66: ("ROR", 1, "$LL"),
  0x68: ("PLA", 0, ""),
  0x69: ("ADC", 1, "#$BB"),
  0x6a: ("ROR", 0, "A"),
  0x6c: ("JMP", 2, "($HHLL)"),
  0x6d: ("ADC", 2, "$HHLL"),
  0x6e: ("ROR", 2, "$HHLL"),
  0x70: ("BVS", 1, "$BB"),
  0x71: ("ADC", 1, "($LL), Y"),
  0x75: ("ADC", 1, "$LL, X"),
  0x76: ("ROR", 1, "$LL, X"),
  0x78: ("SEI", 0, ""),
  0x79: ("ADC", 2, "$HHLL, Y"),
  0x7d: ("ADC", 2, "$HHLL, X"),
  0x7e: ("ROR", 2, "$HHLL, X"),
  0x81: ("STA", 1, "($LL, X)"),
  0x84: ("STY", 1, "$LL"),
  0x85: ("STA", 1, "$LL"),
  0x86: ("STX", 1, "$LL"),
  0x88: ("DEY", 0, ""),
  0x8a: ("TXA", 0, ""),
  0x8c: ("STY", 2, "$HHLL"),
  0x8d: ("STA", 2, "$HHLL"),
  0x8e: ("STX", 2, "$HHLL"),
  0x90: ("BCC", 1, "$BB"),
  0x91: ("STA", 1, "($LL), Y"),
  0x94: ("STY", 1, "$LL, X"),
  0x95: ("STA", 1, "$LL, X"),
  0x96: ("STX", 1, "$LL, Y"),
  0x98: ("TYA", 0, ""),
  0x99: ("STA", 2, "$HHLL, Y"),
  0x9a: ("TXS", 0, ""),
  0x9d: ("STA", 2, "$HHLL, X"),
  0xa0: ("LDY", 1, "#$BB"),
  0xa1: ("LDA", 1, "($LL, X)"),
  0xa2: ("LDX", 1, "#$BB"),
  0xa4: ("LDY", 1, "$LL"),
  0xa5: ("LDA", 1, "$LL"),
  0xa6: ("LDX", 1, "$LL"),
  0xa8: ("TAY", 0, ""),
  0xa9: ("LDA", 1, "#$BB"),
  0xaa: ("TAX", 0, ""),
  0xac: ("LDY", 2, "$HHLL"),
  0xad: ("LDA", 2, "$HHLL"),
  0xae: ("LDX", 2, "$HHLL"),
  0xb0: ("BCS", 1, "$BB"),
  0xb1: ("LDA", 1, "($LL), Y"),
  0xb4: ("LDY", 1, "$LL, X"),
  0xb5: ("LDA", 1, "$LL, X"),
  0xb6: ("LDX", 1, "$LL, Y"),
  0xb8: ("CLV", 0, ""),
  0xb9: ("LDA", 2, "$HHLL, Y"),
  0xba: ("TSX", 0, ""),
  0xbc: ("LDY", 2, "$HHLL, X"),
  0xbd: ("LDA", 2, "$HHLL, X"),
  0xbe: ("LDX", 2, "$HHLL, Y"),
  0xc0: ("CPY", 1, "#$BB"),
  0xc1: ("CMP", 1, "($LL, X)"),
  0xc4: ("CPY", 1, "$LL"),
  0xc5: ("CMP", 1, "$LL"),
  0xc6: ("DEC", 1, "$LL"),
  0xc8: ("INY", 0, ""),
  0xc9: ("CMP", 1, "#$BB"),
  0xca: ("DEX", 0, ""),
  0xcc: ("CPY", 2, "$HHLL"),
  0xcd: ("CMP", 2, "$HHLL"),
  0xce: ("DEC", 2, "$HHLL"),
  0xd0: ("BNE", 1, "$BB"),
  0xd1: ("CMP", 1, "($LL), Y"),
  0xd5: ("CMP", 1, "$LL, X"),
  0xd6: ("DEC", 1, "$LL, X"),
  0xd8: ("CLD", 0, ""),
  0xd9: ("CMP", 2, "$HHLL, Y"),
  0xdd: ("CMP", 2, "$HHLL, X"),
  0xde: ("DEC", 2, "$HHLL, X"),
  0xe0: ("CPX", 1, "#$BB"),
  0xe1: ("SBC", 1, "($LL, X)"),
  0xe4: ("CPX", 1, "$LL"),
  0xe5: ("SBC", 1, "$LL"),
  0xe6: ("INC", 1, "$LL"),
  0xe8: ("INX", 0, ""),
  0xe9: ("SBC", 1, "#$BB"),
  0xea: ("NOP", 0, ""),
  0xec: ("CPX", 2, "$HHLL"),
  0xed: ("SBC", 2, "$HHLL"),
  0xee: ("INC", 2, "$HHLL"),
  0xf0: ("BEQ", 1, "$BB"),
  0xf1: ("SBC", 1, "($LL), Y"),
  0xf5: ("SBC", 1, "$LL, X"),
  0xf6: ("INC", 1, "$LL, X"),
  0xf8: ("SED", 0, ""),
  0xf9: ("SBC", 2, "$HHLL, Y"),
  0xfd: ("SBC", 2, "$HHLL, X"),
  0xfe: ("INC", 2, "$HHLL, X")
}
