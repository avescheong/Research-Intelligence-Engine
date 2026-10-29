"""
Release Candidate Audit & E2E Lifecycle Test
Executes the full RC-01 through RC-06 audit suite within unittest.
"""

import unittest
from pathlib import Path
from engine.adapters.rc_auditor import RCAuditor

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestRCAuditAndE2E(unittest.TestCase):
    def setUp(self):
        self.auditor = RCAuditor(REPO_ROOT)

    def test_rc01_structure(self):
        passed, msg = self.auditor.audit_rc01_structure()
        self.assertTrue(passed, msg)

    def test_rc02_security_zero_pii(self):
        passed, msg = self.auditor.audit_rc02_security()
        self.assertTrue(passed, msg)

    def test_rc03_build_integrity(self):
        passed, msg = self.auditor.audit_rc03_build()
        self.assertTrue(passed, msg)

    def test_rc04_extension_contracts(self):
        passed, msg = self.auditor.audit_rc04_extension()
        self.assertTrue(passed, msg)

    def test_rc05_github_hygiene(self):
        passed, msg = self.auditor.audit_rc05_github()
        self.assertTrue(passed, msg)

    def test_rc06_clean_clone_reproducibility(self):
        passed, msg = self.auditor.audit_rc06_reproducibility()
        self.assertTrue(passed, msg)

if __name__ == "__main__":
    unittest.main()
