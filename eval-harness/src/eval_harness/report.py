# (C) %COMPANY%
"""Scoring and the grade record printed to stdout (one JSON line per grade).

The model only picks the band; code turns it into points here. Each record
carries what produced it (R9): config, file and prompt hashes, reading-rules
version. Never the HTTP headers, which JudgeConfig doesn't hold.
"""

import config
import inputs
import json
import logging
import prompts
import re
import reply
import rubric
import strings

from dataclasses import asdict, dataclass

# CONSTS
LOGGER = logging.getLogger(__name__)
READING_RULES_VERSION = "v1: points must be earned; strictest band wins; Partial = 50% (provisional)"
PROVISIONAL_PARTIAL_FRACTION = 0.5
NO_POINTS = 0.0
LOCATION_FORMAT = "{path}:{line}"
LINE_BREAK = "\n"
FIRST_LINE = 1
TEXT_START = 0
# A quote is located with its whitespace runs allowed to match any whitespace
# in the file, the same way the checks in reply.py compare them.
WHITESPACE_RUN = r"\s+"
# What a location says when there is nothing to cite. Both are real states,
# not missing data, so the record carries the reason instead of a null (R5).
NO_RUBRIC_CONDITION = "none: no band's conditions were met"
NO_ANSWER_GIVEN = "none: the agent gave no answer to this question"


# TYPES
@dataclass(frozen=True)
class Hashes:
    """SHA-256 of every file that shaped a grade."""

    answer_file: str
    rubric: str
    briefing: str
    grader_agents: str
    system_prompt: str
    user_prompt: str


@dataclass(frozen=True)
class RunInfo:
    """What every grade in one run shares: built once per run."""

    run_id: str
    answer_file: str
    reading_rules_version: str
    judge_config: config.JudgeConfig
    hashes: Hashes


@dataclass(frozen=True)
class QuoteLocations:
    """Where each quote was found, as "path:line" (R5).

    Never null. Where there is nothing to cite -- no band's conditions were
    met, or the agent didn't answer -- the field says which, so a reader can
    tell "nothing to point at" from "we failed to look". A quote that passed
    validation and still can't be found is a bug, and fails the grade rather
    than appearing here as missing.
    """

    rubric_quote: str
    answer_quote: str


@dataclass(frozen=True)
class GradeRecord:
    """One grade: one rubric entry, one repeat. Printed as a JSON line."""

    run: RunInfo
    question: int
    heading: str
    max_points: int
    repeat: int
    points: float
    provisional: bool
    reply: reply.Reply
    quotes_at: QuoteLocations


# PUBLIC FUNCTIONS
def score(band: str, max_points: int) -> tuple[float, bool]:
    """Return (points, provisional) for band on a question worth max_points.

    Partial is provisionally half the points until case authors set values.
    """
    LOGGER.debug("score(%s, %d)", band, max_points)
    if band == reply.BAND_FULL:
        return float(max_points), False
    if band == reply.BAND_PARTIAL:
        return max_points * PROVISIONAL_PARTIAL_FRACTION, True
    return NO_POINTS, False


def build_run_info(
    run_id: str, judge_config: config.JudgeConfig, templates: prompts.Prompts, run_files: inputs.RunFiles
) -> RunInfo:
    """Return what every grade in this run shares."""
    LOGGER.debug("build_run_info(%s)", run_id)
    return RunInfo(
        run_id=run_id,
        answer_file=run_files.answer.path,
        reading_rules_version=READING_RULES_VERSION,
        judge_config=judge_config,
        hashes=_hashes(templates, run_files),
    )


def build_record(
    run_info: RunInfo, run_files: inputs.RunFiles, entry: rubric.RubricEntry, repeat: int, judge_reply: reply.Reply
) -> GradeRecord | Exception:
    """Return the grade record for one validated reply, with its quotes
    located, or the error if a validated quote can't be located.
    """
    LOGGER.debug("build_record(Q%d, repeat %d)", entry.number, repeat)
    quotes_at = _quote_locations(run_files, entry, judge_reply)
    if isinstance(quotes_at, Exception):
        LOGGER.error("cannot build the record for Q%d, repeat %d", entry.number, repeat)
        return quotes_at
    points, provisional = score(judge_reply.band, entry.points)
    return GradeRecord(
        run=run_info,
        question=entry.number,
        heading=entry.heading,
        max_points=entry.points,
        repeat=repeat,
        points=points,
        provisional=provisional,
        reply=judge_reply,
        quotes_at=quotes_at,
    )


def quote_location(path: str, text: str, quote: str, start: int = TEXT_START) -> str | Exception:
    """Return "path:line" of quote's first occurrence in text at or after
    start, or the error if quote is empty or isn't there.

    How text wraps its lines is ignored, so a quote the model re-flowed onto
    one line is still located where the file holds it. Reaching the error
    means a quote passed validation that this can't find: the two disagree,
    which is a bug in the harness, not a fault of the judge, so the caller
    fails the grade rather than emitting one with no citation.
    """
    LOGGER.debug("quote_location(%s)", path)
    if strings.is_empty(quote):
        LOGGER.error("cannot locate an empty quote in %s", path)
        return ValueError(f"cannot locate an empty quote in {path}")
    found = _search_quote(text, quote, start)
    if found is None:
        LOGGER.error("cannot locate a validated quote in %s", path)
        return ValueError(f"a validated quote isn't in {path}")
    return LOCATION_FORMAT.format(path=path, line=text.count(LINE_BREAK, TEXT_START, found) + FIRST_LINE)


def emit(record: GradeRecord) -> None:
    """Print record to stdout as one JSON line."""
    LOGGER.debug("emit(Q%d, repeat %d)", record.question, record.repeat)
    print(json.dumps(asdict(record), ensure_ascii=False), flush=True)


# PRIVATE FUNCTIONS
def _search_quote(text: str, quote: str, start: int) -> int | None:
    """Return the offset in text where quote first occurs at or after start,
    matching each run of whitespace in quote against any whitespace in text,
    or None if it isn't there.

    The words are escaped, so a quote holding regex characters is matched as
    the literal text it is.
    """
    words = quote.split()
    if not words:
        return None
    pattern = WHITESPACE_RUN.join(re.escape(word) for word in words)
    found = re.compile(pattern).search(text, start)
    if found is None:
        return None
    return found.start()


def _quote_locations(
    run_files: inputs.RunFiles, entry: rubric.RubricEntry, judge_reply: reply.Reply
) -> QuoteLocations | Exception:
    """Return where both quotes are, or the first error."""
    rubric_quote = _rubric_quote_location(run_files.rubric, entry, judge_reply)
    if isinstance(rubric_quote, Exception):
        return rubric_quote
    answer_quote = _answer_quote_location(run_files.answer, judge_reply)
    if isinstance(answer_quote, Exception):
        return answer_quote
    return QuoteLocations(rubric_quote=rubric_quote, answer_quote=answer_quote)


def _rubric_quote_location(
    rubric_file: inputs.InputFile, entry: rubric.RubricEntry, judge_reply: reply.Reply
) -> str | Exception:
    """Return where the rubric quote is, NO_RUBRIC_CONDITION if no band's
    conditions were met, or the error.

    Searched from the start of this entry, so a phrase repeated in another
    entry isn't matched. entry.text is the text as authored, which is why it
    is still found in the file unchanged.
    """
    if reply.is_zero_default(judge_reply.rubric_quote):
        return NO_RUBRIC_CONDITION
    entry_start = max(rubric_file.text.find(entry.text), TEXT_START)
    return quote_location(rubric_file.path, rubric_file.text, judge_reply.rubric_quote, entry_start)


def _answer_quote_location(answer_file: inputs.InputFile, judge_reply: reply.Reply) -> str | Exception:
    """Return where the answer quote is, NO_ANSWER_GIVEN if the agent didn't
    answer this question, or the error.
    """
    if strings.is_empty(judge_reply.answer_quote):
        return NO_ANSWER_GIVEN
    return quote_location(answer_file.path, answer_file.text, judge_reply.answer_quote)


def _hashes(templates: prompts.Prompts, run_files: inputs.RunFiles) -> Hashes:
    """Return the hashes of every file that shapes a grade."""
    return Hashes(
        answer_file=run_files.answer.sha256,
        rubric=run_files.rubric.sha256,
        briefing=run_files.briefing.sha256,
        grader_agents=run_files.grader_agents.sha256,
        system_prompt=templates.system.sha256,
        user_prompt=templates.user.sha256,
    )
