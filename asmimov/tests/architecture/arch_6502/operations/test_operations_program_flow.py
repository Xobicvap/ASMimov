import unittest
from tests.architecture.arch_6502.operations import test_operations
from architecture.arch_6502.cpu import operations, cpu_container

class OperationsProgramFlowTest(test_operations.OperationsTest):

  def branch_fxn_test(self, metadata, pc_metadata, operation, expected_pc, expected_cycles):
    inst = self.Instruction(metadata, pc_metadata)
    result = operation(None, inst)

    pc = result["PC"]
    cycles = result["cycles"]

    self.assertEqual(pc, expected_pc)
    self.assertEqual(cycles, expected_cycles)

  def non_branching_test(self, operation, branch_cond):
    # the dest (3rd) param here is the PC... shades of apple ii assembly :p
    metadata = (0x04, branch_cond, 0x0800)
    pc_metadata = (2, 2)
    expected_pc = 0x0802
    expected_cycles = 2

    self.branch_fxn_test(metadata, pc_metadata, operation, expected_pc, expected_cycles)

  def forward_branching_test(self, operation, branch_cond):
    metadata = (0x04, branch_cond, 0x0800)
    pc_metadata = (2, 2)
    expected_pc = 0x0804
    expected_cycles = 3 

    self.branch_fxn_test(metadata, pc_metadata, operation, expected_pc, expected_cycles)

  def forward_branching_test_page_cross(self, operation, branch_cond):
    metadata = (0x70, branch_cond, 0x08a0)
    pc_metadata = (2, 2)
    expected_pc = 0x0910
    expected_cycles = 4

    self.branch_fxn_test(metadata, pc_metadata, operation, expected_pc, expected_cycles)

  def negative_branching_test(self, operation, branch_cond):
    metadata = (0xfd, branch_cond, 0x0803)
    pc_metadata = (2, 2)
    expected_pc = 0x800
    expected_cycles = 3

    self.branch_fxn_test(metadata, pc_metadata, operation, expected_pc, expected_cycles)

  def negative_branching_test_page_cross(self, operation, branch_cond):
    metadata = (0xfc, branch_cond, 0x0803)
    pc_metadata = (2, 2)
    expected_pc = 0x7ff
    expected_cycles = 4

    self.branch_fxn_test(metadata, pc_metadata, operation, expected_pc, expected_cycles)

  def test_bmi_does_not_branch(self):
    self.non_branching_test(operations.bmi, 0)

  def test_bmi_branches_forward(self):
    self.forward_branching_test(operations.bmi, 1)

  def test_bmi_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bmi, 1)
  
  def test_bmi_branches_negative(self):
    self.negative_branching_test(operations.bmi, 1)

  def test_bmi_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bmi, 1)

  def test_bvs_does_not_branch(self):
    self.non_branching_test(operations.bvs, 0)

  def test_bvs_branches_forward(self):
    self.forward_branching_test(operations.bvs, 1)

  def test_bvs_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bvs, 1)
  
  def test_bvs_branches_negative(self):
    self.negative_branching_test(operations.bvs, 1)

  def test_bvs_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bvs, 1)

  def test_bcs_does_not_branch(self):
    self.non_branching_test(operations.bcs, 0)

  def test_bcs_branches_forward(self):
    self.forward_branching_test(operations.bcs, 1)

  def test_bcs_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bcs, 1)
  
  def test_bcs_branches_negative(self):
    self.negative_branching_test(operations.bcs, 1)

  def test_bcs_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bcs, 1)

  def test_beq_does_not_branch(self):
    self.non_branching_test(operations.beq, 0)

  def test_beq_branches_forward(self):
    self.forward_branching_test(operations.beq, 1)

  def test_beq_branches_forward_page_cross(self):
    self.forward_branching_test(operations.beq, 1)
  
  def test_beq_branches_negative(self):
    self.negative_branching_test(operations.beq, 1)

  def test_beq_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.beq, 1)

  def test_bpl_does_not_branch(self):
    self.non_branching_test(operations.bpl, 1)

  def test_bpl_branches_forward(self):
    self.forward_branching_test(operations.bpl, 0)

  def test_bpl_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bpl, 0)
  
  def test_bpl_branches_negative(self):
    self.negative_branching_test(operations.bpl, 0)

  def test_bpl_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bpl, 0)

  def test_bvc_does_not_branch(self):
    self.non_branching_test(operations.bvc, 1)

  def test_bvc_branches_forward(self):
    self.forward_branching_test(operations.bvc, 0)

  def test_bvc_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bvc, 0)
  
  def test_bvc_branches_negative(self):
    self.negative_branching_test(operations.bvc, 0)

  def test_bvc_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bvc, 0)

  def test_bcc_does_not_branch(self):
    self.non_branching_test(operations.bcc, 1)

  def test_bcc_branches_forward(self):
    self.forward_branching_test(operations.bcc, 0)

  def test_bcc_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bcc, 0)
  
  def test_bcc_branches_negative(self):
    self.negative_branching_test(operations.bcc, 0)

  def test_bcc_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bcc, 0)

  def test_bne_does_not_branch(self):
    self.non_branching_test(operations.bne, 1)

  def test_bne_branches_forward(self):
    self.forward_branching_test(operations.bne, 0)

  def test_bne_branches_forward_page_cross(self):
    self.forward_branching_test(operations.bne, 0)
  
  def test_bne_branches_negative(self):
    self.negative_branching_test(operations.bne, 0)

  def test_bne_branches_negative_page_cross(self):
    self.negative_branching_test_page_cross(operations.bne, 0)

  # "i don't think there's a lot of ways these could go wrong... ?"
  # HAHAHA famous last words after i converted these to use real
  # cpu container classes and got rid of the stupid push/pop nonsense
  def test_jsr(self):
    metadata = (0x9000, 0x8000, "PC")
    inst = self.Instruction(metadata)

    system = cpu_container.CPUContainer(None, None, None, 0x8000, None, 0xd3)

    result = operations.jsr(system, inst)
    dpc = result["PC"]
    stack_ptr = result["SP"]
    stack_ptr_addr = stack_ptr + 0x100
    pc_hi_addr = stack_ptr_addr + 2
    pc_lo_addr = stack_ptr_addr + 1

    self.assertEqual(dpc, 0x9000)
    self.assertEqual(stack_ptr, 0xd1)
    self.assertEqual(result[pc_lo_addr], 0x02)
    self.assertEqual(result[pc_hi_addr], 0x80)


  def test_jmp(self):
    metadata = (0x1234, None, "PC")
    inst = self.Instruction(metadata)

    result = operations.jmp(None, inst)
    dpc = result["PC"]

    self.assertEqual(dpc, 0x1234)

  def test_brk(self):
    metadata = (0b01001001, 0x7800, "PC")
    inst = self.Instruction(metadata)

    system = cpu_container.CPUContainer(None, None, None, 0x7802, 0b01001001, 0xf0, {0xfffe: 0x80, 0xffff: 0x98})

    result = operations.brk(system, inst)

    dpc = result["PC"]
    sp = result["SP"]

    stack_ptr_addr = sp + 0x100

    status_addr = stack_ptr_addr + 1
    pc_addr_lo = stack_ptr_addr + 2
    pc_addr_hi = stack_ptr_addr + 3

    self.assertEqual(dpc, 0x9880)
    self.assertTrue(pc_addr_hi in result)
    self.assertEqual(result[pc_addr_hi], 0x78)
    self.assertEqual(result[pc_addr_lo], 0x02)
    self.assertEqual(result[status_addr], 0b01111001)
    self.assertEqual(sp, 0xed, str(sp) + " " + str(result))

  def test_rti(self):
    metadata = (0x0fc, None, None)
    inst = self.Instruction(metadata)

    system = cpu_container.CPUContainer(None, None, None, None, None, 0xfc,
                                        {0x01fd: 0b10110101, 0x01fe: 0x00, 0x01ff: 0xa0})

    self.assertEqual(0, system.cpu_register("P"))
    result = operations.rti(system, inst)
    dpc = result["PC"]
    status = result["P"]
    sp = result["SP"]

    self.assertEqual(dpc, 0xa000)
    self.assertEqual(status, 0b10000101)
    self.assertEqual(result[0x1fd], 0)

    self.assertEqual(result[0x1fe], 0)
    self.assertEqual(result[0x1ff], 0)
    self.assertEqual(sp, 0xff)

  def test_rts(self):
    metadata = (0x23ff, None, "PC")
    inst = self.Instruction(metadata)
    system = cpu_container.CPUContainer(None, None, None, None, None, 0x7f)

    result = operations.rts(system, inst)
    dpc = result["PC"]
    dsp = result["SP"]
    lo_byte = result[0x17f]
    hi_byte = result[0x180]

    self.assertEqual(dpc, 0x2400)
    self.assertEqual(dsp, 0x81)
    self.assertEqual(lo_byte, 0)
    self.assertEqual(hi_byte, 0)


