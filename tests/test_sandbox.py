"""Unit tests for agent-speculative-edit-sandbox."""
import unittest
from agent_speculative_edit_sandbox.sandbox import SpeculativeSandbox


class TestSpeculativeSandbox(unittest.TestCase):
    def setUp(self):
        self.sb = SpeculativeSandbox()

    def test_valid_code_staging(self):
        res = self.sb.stage_file("test.py", "x = [i * 2 for i in range(10)]")
        self.assertTrue(res.valid)
        self.assertGreater(res.ast_nodes, 0)
        self.assertEqual(self.sb.get_staged_content("test.py"), "x = [i * 2 for i in range(10)]")

    def test_invalid_syntax_rejected(self):
        res = self.sb.stage_file("bad.py", "def foo(:\n  pass")
        self.assertFalse(res.valid)
        self.assertIn("SyntaxError", res.error)
        self.assertIsNone(self.sb.get_staged_content("bad.py"))
