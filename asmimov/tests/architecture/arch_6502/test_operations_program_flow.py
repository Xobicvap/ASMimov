import unittest
from tests.architecture.arch_6502 import test_operations
from architecture.arch_6502 import operations

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

  # i don't think there's a lot of ways these could go wrong... ?
  def test_jsr(self):
    metadata = (0x9000, 0x8000, "PC")
    inst = self.Instruction(metadata)

    result = operations.jsr(None, inst)
    dpc = result["PC"]
    dpush = result["push"]

    self.assertEqual(dpc, 0x9000)
    self.assertEqual(len(dpush), 2)
    self.assertEqual(dpush[0], 0x80)
    self.assertEqual(dpush[1], 0x02)

  def test_rti(self):
    metadata = (0x0fc, None, None)
    inst = self.Instruction(metadata)

    system = self.TestSystem(None, {0x01fd: 0b10110101, 0x01fe: 0x00, 0x01ff: 0xa0})

    result = operations.rti(system, inst)
    dpc = result["PC"]
    status = result["P"]
    # i think this is 3 bytes? but the docs say Processor Status WORD... why WORD?
    self.assertEqual(result["pop"], 3)
    self.assertEqual(dpc, 0xa000)
    self.assertEqual(status, 0b10000101)


  def test_rts(self):
    metadata = (0x23ff, None, "PC")
    inst = self.Instruction(metadata)

    result = operations.rts(None, inst)
    dpc = result["PC"]
    self.assertEqual(result["pop"], 2)
    self.assertEqual(dpc, 0x2400)


