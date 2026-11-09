# (C) %COMPANY%
"""Tests for strings.py."""

import strings
import unittest

# CONSTS
WRAPPED = "Correct event cited, no explanation of why the path\nitself is the tell."
REFLOWED = "Correct event cited, no explanation of why the path itself is the tell."


# TYPES
class NormalizeWhitespaceTest(unittest.TestCase):
    """Tests for normalize_whitespace."""

    def test_wrapped_and_reflowed_match(self) -> None:
        """A hard-wrapped line and the same sentence on one line normalize alike."""
        self.assertEqual(strings.normalize_whitespace(WRAPPED), strings.normalize_whitespace(REFLOWED))

    def test_collapses_runs(self) -> None:
        """Runs of spaces, tabs and newlines each become one space."""
        self.assertEqual(strings.normalize_whitespace("a  \t\n b"), "a b")

    def test_trims_edges(self) -> None:
        """Leading and trailing whitespace is removed."""
        self.assertEqual(strings.normalize_whitespace("\n  a b  \n"), "a b")

    def test_empty(self) -> None:
        """Whitespace-only text normalizes to the empty string."""
        self.assertEqual(strings.normalize_whitespace(" \n\t "), "")

    def test_single_word_unchanged(self) -> None:
        """Text with no whitespace to collapse comes back as it was."""
        self.assertEqual(strings.normalize_whitespace("Zero"), "Zero")


class IsEmptyTest(unittest.TestCase):
    """Tests for is_empty."""

    def test_none_and_blank_are_empty(self) -> None:
        """None, "" and whitespace-only all count as empty."""
        self.assertTrue(strings.is_empty(None))
        self.assertTrue(strings.is_empty(""))
        self.assertTrue(strings.is_empty(" \n "))

    def test_text_is_not_empty(self) -> None:
        """Any non-whitespace character makes it non-empty."""
        self.assertFalse(strings.is_empty("a"))


# INLINE RUN
if __name__ == "__main__":
    unittest.main()
