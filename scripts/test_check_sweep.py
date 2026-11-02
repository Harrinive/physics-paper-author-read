r"""Tests of ``check_sweep.py``: a complete table passes, every gap fails.

Run with ``python3 -m pytest`` from this folder.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import check_sweep as cs


class TestSweep(unittest.TestCase):
    """Extraction and the completeness check."""

    def setUp(self):
        """Write a source with three matches on two lines, and extract them."""
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "a.tex"
        self.source.write_text("the copy and the copy\nnothing here\none copy\n")
        self.occ = self.root / "occ.tsv"
        self.ver = self.root / "ver.tsv"
        with contextlib.redirect_stdout(io.StringIO()):
            cs.main(["extract", "--pattern", "copy", "--out", str(self.occ), str(self.source)])

    def tearDown(self):
        """Remove the temporary folder."""
        self.tmp.cleanup()

    def check(self, rows):
        """Write a verdict table and return the exit code of ``check``."""
        body = "\n".join("\t".join(r) for r in rows)
        self.ver.write_text("id\tverdict\treason\n" + body + "\n")
        with contextlib.redirect_stdout(io.StringIO()):
            return cs.main(["check", str(self.occ), str(self.ver)])

    def test_each_match_gets_an_identifier(self):
        """Two matches on one line are two occurrences."""
        rows = cs.read_table(str(self.occ))
        self.assertEqual([r["id"] for r in rows], ["O001", "O002", "O003"])
        self.assertEqual([r["line"] for r in rows], ["1", "1", "3"])

    def test_complete_table_passes(self):
        """One verdict with a reason per occurrence passes."""
        self.assertEqual(self.check([("O001", "fix", "a"), ("O002", "keep", "b"),
                                     ("O003", "keep", "c")]), 0)

    def test_missing_row_fails(self):
        """A skipped occurrence fails."""
        self.assertEqual(self.check([("O001", "fix", "a"), ("O002", "keep", "b")]), 1)

    def test_unknown_id_fails(self):
        """A row for no occurrence fails."""
        self.assertEqual(self.check([("O001", "fix", "a"), ("O002", "keep", "b"),
                                     ("O003", "keep", "c"), ("O004", "keep", "d")]), 1)

    def test_repeated_id_fails(self):
        """Two rows for one occurrence fail."""
        self.assertEqual(self.check([("O001", "fix", "a"), ("O001", "keep", "b"),
                                     ("O002", "keep", "c"), ("O003", "keep", "d")]), 1)

    def test_bad_verdict_and_empty_reason_fail(self):
        """A verdict outside the list, or no reason, fails."""
        self.assertEqual(self.check([("O001", "maybe", "a"), ("O002", "keep", "b"),
                                     ("O003", "keep", "c")]), 1)
        self.assertEqual(self.check([("O001", "fix", ""), ("O002", "keep", "b"),
                                     ("O003", "keep", "c")]), 1)


if __name__ == "__main__":
    unittest.main()
