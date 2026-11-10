# (C) %COMPANY%
"""Tests for reply.py."""

import json
import reply
import rubric
import strings
import unittest

# CONSTS
# A rubric entry wrapped the way the real ones are: two of its conditions
# break mid-sentence, which is what made re-flowed quotes fail before.
RUBRIC_TEXT = """# Grading schema

## Q1 - Execution (15 pts)
**Expected:** Event ID 4688 on the host.
**Full credit:** Correct process and path, AND explains the
masquerading tell.
**Partial:** Correct event cited, no explanation of why the path
itself is the tell.
**Zero:** Wrong process cited.
"""
# A second entry with no Partial band, for the band check.
RUBRIC_TEXT_NO_PARTIAL = """# Grading schema

## Q2 - Scope (10 pts)
**Full credit:** Names every affected host.
**Zero:** Names none of them.
"""
ANSWER_TEXT = """# Answers

## Q1
The process was ARMHelper.exe, launched from the user's
AppData directory.
"""
WRAPPED_RUBRIC_QUOTE = "Correct event cited, no explanation of why the path\nitself is the tell."
REFLOWED_RUBRIC_QUOTE = "Correct event cited, no explanation of why the path itself is the tell."
REFLOWED_ANSWER_QUOTE = "The process was ARMHelper.exe, launched from the user's AppData directory."
ABSENT_QUOTE = "Mentions the registry run key."
REASONS = "The answer names the event but never explains the path."
BAND_PARTIAL = "partial"
BAND_FULL = "full"
BAND_ZERO = "zero"
CONFIDENCE = "high"
EMPTY = ""


# TYPES
class ParseReplyTest(unittest.TestCase):
    """Tests for parse_reply."""

    def setUp(self) -> None:
        """Parse the fixture rubrics into the entries the checks run against."""
        self.entry = _first_entry(RUBRIC_TEXT)
        self.entry_no_partial = _first_entry(RUBRIC_TEXT_NO_PARTIAL)
        self.answer = _answer_words(ANSWER_TEXT)

    def test_rubric_quote_is_kept_as_sent(self) -> None:
        """The quote is carried through unchanged, for the record to show."""
        parsed = reply.parse_reply(_raw(rubric_quote=REFLOWED_RUBRIC_QUOTE), self.entry, self.answer)
        self.assertEqual(parsed.rubric_quote, REFLOWED_RUBRIC_QUOTE)

    def test_restated_rubric_quote_is_accepted(self) -> None:
        """A condition the judge reworded no longer fails the grade."""
        restated = "Correct event cites, no explantion of why the path itself is the tell"
        parsed = reply.parse_reply(_raw(rubric_quote=restated), self.entry, self.answer)
        self.assertIsInstance(parsed, reply.Reply)

    def test_wrapped_rubric_quote_is_accepted(self) -> None:
        """A quote copied with the rubric's own line break is fine too."""
        parsed = reply.parse_reply(_raw(rubric_quote=WRAPPED_RUBRIC_QUOTE), self.entry, self.answer)
        self.assertIsInstance(parsed, reply.Reply)

    def test_unrelated_rubric_quote_is_accepted(self) -> None:
        """rubric_quote is not validated at all: the record shows it instead."""
        parsed = reply.parse_reply(_raw(rubric_quote=ABSENT_QUOTE), self.entry, self.answer)
        self.assertIsInstance(parsed, reply.Reply)

    def test_empty_rubric_quote_is_accepted(self) -> None:
        """Even an empty quote grades; the citation comes from the rubric."""
        parsed = reply.parse_reply(_raw(rubric_quote=EMPTY), self.entry, self.answer)
        self.assertIsInstance(parsed, reply.Reply)

    def test_zero_default_with_band_zero_is_accepted(self) -> None:
        """The no-band-met marker is carried through when the band is zero."""
        raw = _raw(rubric_quote=reply.ZERO_DEFAULT, band=BAND_ZERO)
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), reply.Reply)

    def test_reflowed_answer_quote_is_accepted(self) -> None:
        """The answer file is agent-wrapped, so wrapping can't decide this."""
        raw = _raw(answer_quote=REFLOWED_ANSWER_QUOTE)
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), reply.Reply)

    def test_restated_answer_quote_is_accepted(self) -> None:
        """A quote the judge reworded still came from the answer file."""
        restated = "The proces was ARMHelper.exe, launched from the user's AppData directory"
        self.assertIsInstance(reply.parse_reply(_raw(answer_quote=restated), self.entry, self.answer), reply.Reply)

    def test_invented_answer_quote_is_rejected(self) -> None:
        """A quote sharing almost nothing with the answer file was invented."""
        raw = _raw(answer_quote=ABSENT_QUOTE)
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), Exception)

    def test_fabricated_answer_quote_is_rejected(self) -> None:
        """Grading an answer the agent never gave must not pass."""
        raw = _raw(answer_quote="The attacker exfiltrated the database over SMB to 10.0.0.9")
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), Exception)

    def test_empty_answer_quote_with_band_zero_is_accepted(self) -> None:
        """A question the agent didn't answer is a legitimate zero."""
        raw = _raw(rubric_quote=reply.ZERO_DEFAULT, answer_quote=EMPTY, band=BAND_ZERO)
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), reply.Reply)

    def test_empty_answer_quote_with_other_band_is_rejected(self) -> None:
        """Credit can't rest on an answer the judge didn't quote."""
        raw = _raw(answer_quote=EMPTY, band=BAND_PARTIAL)
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), Exception)

    def test_empty_reasons_is_rejected(self) -> None:
        """Every grade carries a rationale (R5)."""
        raw = _raw(reasons=EMPTY)
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), Exception)

    def test_whitespace_only_reasons_is_rejected(self) -> None:
        """Whitespace isn't a rationale."""
        raw = _raw(reasons=" \n ")
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), Exception)

    def test_band_missing_from_entry_is_rejected(self) -> None:
        """An entry with no Partial band can't be graded partial."""
        raw = _raw(rubric_quote="Names every affected host.", band=BAND_PARTIAL)
        self.assertIsInstance(reply.parse_reply(raw, self.entry_no_partial, self.answer), Exception)

    def test_unknown_band_is_rejected(self) -> None:
        """Only the three named bands are allowed."""
        self.assertIsInstance(reply.parse_reply(_raw(band="bonus"), self.entry, self.answer), Exception)

    def test_unknown_confidence_is_rejected(self) -> None:
        """Only the three named confidence levels are allowed."""
        raw = _raw(confidence="certain")
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), Exception)

    def test_missing_field_is_rejected(self) -> None:
        """The reply must have exactly the five fields."""
        fields = _fields()
        del fields["confidence"]
        parsed = reply.parse_reply(json.dumps(fields), self.entry, self.answer)
        self.assertIsInstance(parsed, Exception)

    def test_extra_field_is_rejected(self) -> None:
        """An unexpected field means the reply isn't the shape we asked for."""
        fields = _fields()
        fields["points"] = "15"
        parsed = reply.parse_reply(json.dumps(fields), self.entry, self.answer)
        self.assertIsInstance(parsed, Exception)

    def test_non_string_field_is_rejected(self) -> None:
        """Every field is a string, so a number fails."""
        fields = _fields()
        fields["confidence"] = 1
        parsed = reply.parse_reply(json.dumps(fields), self.entry, self.answer)
        self.assertIsInstance(parsed, Exception)

    def test_not_json_is_rejected(self) -> None:
        """A reply that isn't JSON fails."""
        self.assertIsInstance(reply.parse_reply("not json", self.entry, self.answer), Exception)

    def test_json_but_not_an_object_is_rejected(self) -> None:
        """A JSON list isn't a reply."""
        self.assertIsInstance(reply.parse_reply("[1, 2]", self.entry, self.answer), Exception)


class CodeFenceTest(unittest.TestCase):
    """Tests that a reply wrapped in a fence or prose still parses."""

    def setUp(self) -> None:
        """Parse the fixture rubric and answer the checks run against."""
        self.entry = _first_entry(RUBRIC_TEXT)
        self.answer = _answer_words(ANSWER_TEXT)

    def test_fenced_reply_is_accepted(self) -> None:
        """A reply inside a ```json fence parses rather than killing the run."""
        raw = f"```json\n{_raw()}\n```"
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), reply.Reply)

    def test_bare_fenced_reply_is_accepted(self) -> None:
        """A fence with no language tag works too."""
        raw = f"```\n{_raw()}\n```"
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), reply.Reply)

    def test_prose_around_the_object_is_accepted(self) -> None:
        """A sentence before or after the object doesn't lose the grade."""
        raw = f"Here is my assessment:\n{_raw()}\nLet me know if you need more."
        self.assertIsInstance(reply.parse_reply(raw, self.entry, self.answer), reply.Reply)

    def test_plain_object_still_parses(self) -> None:
        """The happy path is unchanged."""
        self.assertIsInstance(reply.parse_reply(_raw(), self.entry, self.answer), reply.Reply)

    def test_no_object_at_all_is_rejected(self) -> None:
        """Text with no JSON object in it still fails."""
        self.assertIsInstance(reply.parse_reply("I cannot grade this.", self.entry, self.answer), Exception)


class IsZeroDefaultTest(unittest.TestCase):
    """Tests for is_zero_default."""

    def test_exact_marker(self) -> None:
        """The marker as the prompt asks for it."""
        self.assertTrue(reply.is_zero_default(reply.ZERO_DEFAULT))

    def test_respaced_marker(self) -> None:
        """The marker with its whitespace changed is still the marker."""
        self.assertTrue(reply.is_zero_default("  Zero -\tdefault "))

    def test_other_text(self) -> None:
        """A real rubric condition isn't the marker."""
        self.assertFalse(reply.is_zero_default(REFLOWED_RUBRIC_QUOTE))

    def test_different_words(self) -> None:
        """Only whitespace is forgiven, not wording."""
        self.assertFalse(reply.is_zero_default("Zero by default"))


# PRIVATE FUNCTIONS
def _first_entry(rubric_text: str) -> rubric.RubricEntry:
    """Return the first entry of rubric_text, parsed the way a run parses it."""
    return rubric.read_rubric_entries_as_list(rubric_text)[0]


def _answer_words(text: str) -> frozenset[str]:
    """Return text as the answer file's words would hold it."""
    return strings.distinct_words(text)


def _fields(
    rubric_quote: str = REFLOWED_RUBRIC_QUOTE,
    answer_quote: str = REFLOWED_ANSWER_QUOTE,
    reasons: str = REASONS,
    band: str = BAND_PARTIAL,
    confidence: str = CONFIDENCE,
) -> dict[str, object]:
    """Return a valid reply's fields, with any of them overridden."""
    return {
        "rubric_quote": rubric_quote,
        "answer_quote": answer_quote,
        "reasons": reasons,
        "band": band,
        "confidence": confidence,
    }


def _raw(**overrides: str) -> str:
    """Return a reply as the model would send it: one JSON object."""
    return json.dumps(_fields(**overrides))


# INLINE RUN
if __name__ == "__main__":
    unittest.main()
