# (C) %COMPANY%
"""Tests for report.py."""

import config
import inputs
import report
import reply
import rubric
import strings
import unittest

# CONSTS
RUBRIC_PATH = "grading_schema.md"
ANSWER_PATH = "QUESTION_ANSWERS.md"
# "**Partial:**" sits on line 7, and its condition wraps onto line 8.
RUBRIC_TEXT = """# Grading schema

## Q1 - Execution (15 pts)
**Expected:** Event ID 4688 on the host.
**Full credit:** Correct process and path, AND explains the
masquerading tell.
**Partial:** Correct event cited, no explanation of why the path
itself is the tell.
**Zero:** Wrong process cited.
"""
PARTIAL_LINE = 7
ZERO_LINE = 9
ZERO_CONDITION = "**Zero:** Wrong process cited."
ANSWER_TEXT = """# Answers

## Q1
The process was ARMHelper.exe, launched from the user's
AppData directory.
"""
ANSWER_LINE = 4
REFLOWED_RUBRIC_QUOTE = "Correct event cited, no explanation of why the path itself is the tell."
REFLOWED_ANSWER_QUOTE = "The process was ARMHelper.exe, launched from the user's AppData directory."
ABSENT_QUOTE = "Mentions the registry run key."
REASONS = "The answer names the event but never explains the path."
RUN_ID = "20261109T120000Z-abc123"
HASH = "0" * 64
MAX_POINTS = 15
PARTIAL_POINTS = 7.5
NO_POINTS = 0.0
REPEAT = 1
FIRST_LINE = 1
EMPTY = ""
REGEX_TEXT = "a (b) [c] d\n"
REGEX_QUOTE = "(b) [c]"


# TYPES
class QuoteLocationTest(unittest.TestCase):
    """Tests for quote_location."""

    def test_reflowed_quote_keeps_its_line(self) -> None:
        """A quote the model re-flowed is still located where the file wraps it."""
        found = report.quote_location(RUBRIC_PATH, RUBRIC_TEXT, REFLOWED_RUBRIC_QUOTE)
        self.assertEqual(found, f"{RUBRIC_PATH}:{PARTIAL_LINE}")

    def test_quote_as_written_is_located(self) -> None:
        """A quote copied with the file's own line break works too."""
        found = report.quote_location(RUBRIC_PATH, RUBRIC_TEXT, ZERO_CONDITION)
        self.assertEqual(found, f"{RUBRIC_PATH}:{ZERO_LINE}")

    def test_answer_quote_line(self) -> None:
        """The answer file is located the same way."""
        found = report.quote_location(ANSWER_PATH, ANSWER_TEXT, REFLOWED_ANSWER_QUOTE)
        self.assertEqual(found, f"{ANSWER_PATH}:{ANSWER_LINE}")

    def test_absent_quote_is_an_error(self) -> None:
        """A quote that isn't there fails instead of returning no location."""
        found = report.quote_location(RUBRIC_PATH, RUBRIC_TEXT, ABSENT_QUOTE)
        self.assertIsInstance(found, Exception)

    def test_empty_quote_is_an_error(self) -> None:
        """An empty quote has no location, and saying so is an error."""
        self.assertIsInstance(report.quote_location(RUBRIC_PATH, RUBRIC_TEXT, EMPTY), Exception)

    def test_regex_characters_are_literal(self) -> None:
        """A quote holding regex characters is matched as the text it is."""
        found = report.quote_location(RUBRIC_PATH, REGEX_TEXT, REGEX_QUOTE)
        self.assertEqual(found, f"{RUBRIC_PATH}:{FIRST_LINE}")

    def test_search_starts_at_start(self) -> None:
        """A quote before start isn't matched."""
        found = report.quote_location(RUBRIC_PATH, RUBRIC_TEXT, "Wrong process cited.", len(RUBRIC_TEXT))
        self.assertIsInstance(found, Exception)


class ScoreTest(unittest.TestCase):
    """Tests for score."""

    def test_full(self) -> None:
        """Full credit earns every point and isn't provisional."""
        self.assertEqual(report.score(reply.BAND_FULL, MAX_POINTS), (float(MAX_POINTS), False))

    def test_partial(self) -> None:
        """Partial is provisionally half the points."""
        self.assertEqual(report.score(reply.BAND_PARTIAL, MAX_POINTS), (PARTIAL_POINTS, True))

    def test_zero(self) -> None:
        """Zero earns nothing and isn't provisional."""
        self.assertEqual(report.score(reply.BAND_ZERO, MAX_POINTS), (NO_POINTS, False))


class BuildRecordTest(unittest.TestCase):
    """Tests for build_record: every record carries both citations."""

    def setUp(self) -> None:
        """Build the entry, files and run info one record needs."""
        self.entry = rubric.read_rubric_entries_as_list(RUBRIC_TEXT)[0]
        self.run_files = _run_files()
        self.run_info = _run_info()

    def test_both_quotes_are_located(self) -> None:
        """A graded reply gets a real "path:line" for each quote."""
        record = report.build_record(self.run_info, self.run_files, self.entry, REPEAT, _reply())
        self.assertEqual(record.quotes_at.rubric_quote, f"{RUBRIC_PATH}:{PARTIAL_LINE}")
        self.assertEqual(record.quotes_at.answer_quote, f"{ANSWER_PATH}:{ANSWER_LINE}")

    def test_zero_default_says_so(self) -> None:
        """No band's conditions met: the citation names that, and isn't null."""
        judge_reply = _reply(rubric_quote=reply.ZERO_DEFAULT, band=reply.BAND_ZERO)
        record = report.build_record(self.run_info, self.run_files, self.entry, REPEAT, judge_reply)
        self.assertEqual(record.quotes_at.rubric_quote, report.NO_RUBRIC_CONDITION)

    def test_missing_answer_says_so(self) -> None:
        """No answer given: the citation names that, and isn't null."""
        judge_reply = _reply(rubric_quote=reply.ZERO_DEFAULT, answer_quote=EMPTY, band=reply.BAND_ZERO)
        record = report.build_record(self.run_info, self.run_files, self.entry, REPEAT, judge_reply)
        self.assertEqual(record.quotes_at.answer_quote, report.NO_ANSWER_GIVEN)

    def test_unlocatable_quote_fails_the_record(self) -> None:
        """A quote that can't be found is a bug, so no record is emitted."""
        judge_reply = _reply(rubric_quote=ABSENT_QUOTE)
        record = report.build_record(self.run_info, self.run_files, self.entry, REPEAT, judge_reply)
        self.assertIsInstance(record, Exception)

    def test_points_come_from_the_band(self) -> None:
        """Code scores the band the model picked."""
        record = report.build_record(self.run_info, self.run_files, self.entry, REPEAT, _reply())
        self.assertEqual(record.points, PARTIAL_POINTS)
        self.assertTrue(record.provisional)


# PRIVATE FUNCTIONS
def _input_file(path: str, text: str) -> inputs.InputFile:
    """Return text as a read input file, normalized the way a run reads it."""
    return inputs.InputFile(
        path=path,
        text=text,
        sha256=HASH,
        normalized_text=strings.normalize_whitespace(text),
    )


def _run_files() -> inputs.RunFiles:
    """Return the four files a record is built from. Only two are read here."""
    rubric_file = _input_file(RUBRIC_PATH, RUBRIC_TEXT)
    return inputs.RunFiles(
        answer=_input_file(ANSWER_PATH, ANSWER_TEXT),
        rubric=rubric_file,
        briefing=rubric_file,
        grader_agents=rubric_file,
    )


def _run_info() -> report.RunInfo:
    """Return the run info every record in a run shares."""
    return report.RunInfo(
        run_id=RUN_ID,
        answer_file=ANSWER_PATH,
        reading_rules_version=report.READING_RULES_VERSION,
        judge_config=config.JudgeConfig(
            model_name="qwen", provider_url="http://localhost", model_version="v1",
            k=1, max_tokens=1024, temperature=0.0,
        ),
        hashes=report.Hashes(
            answer_file=HASH, rubric=HASH, briefing=HASH,
            grader_agents=HASH, system_prompt=HASH, user_prompt=HASH,
        ),
    )


def _reply(
    rubric_quote: str = REFLOWED_RUBRIC_QUOTE,
    answer_quote: str = REFLOWED_ANSWER_QUOTE,
    band: str = reply.BAND_PARTIAL,
) -> reply.Reply:
    """Return a validated reply, with any of its fields overridden."""
    return reply.Reply(
        rubric_quote=rubric_quote,
        answer_quote=answer_quote,
        reasons=REASONS,
        band=band,
        confidence="high",
    )


# INLINE RUN
if __name__ == "__main__":
    unittest.main()
