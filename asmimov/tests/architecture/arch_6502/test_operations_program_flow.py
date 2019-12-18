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

