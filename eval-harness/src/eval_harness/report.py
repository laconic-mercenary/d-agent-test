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
# What a citation says when there is nothing to cite. Both are real states,
# not missing data, so the record carries the reason instead of a null (R5).
NO_RUBRIC_CONDITION = "none: no band's conditions were met"
NO_ANSWER_GIVEN = "none: the agent gave no answer to this question"
# How exactly the judge's answer quote matched the answer file. Approximate
# means the quote was restated, so the line is the best-matching one rather
# than the quote's own: still a usable pointer, and labelled as what it is.
MATCH_EXACT = "exact"
MATCH_APPROXIMATE = "approximate"
NO_SHARED_WORDS = -1
# Which label states each band's condition. Unlike reply.BAND_LABELS, this
# includes zero: an entry needn't state a Zero condition, and when it doesn't
# there is nothing to cite.
CONDITION_LABELS = (
    (reply.BAND_FULL, rubric.LABEL_FULL_CREDIT),
    (reply.BAND_PARTIAL, rubric.LABEL_PARTIAL),
    (reply.BAND_ZERO, rubric.LABEL_ZERO),
)


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
class Condition:
    """What the rubric requires for the band that was awarded (R5).

    Read from the rubric, not from the judge's reply, so it is exact however
    loosely the judge restated it. Put beside reply.rubric_quote in the
    record: if the judge quoted a different band's condition, the two sit
    side by side and don't match.

    Never null. Where the entry states no condition for the band -- no
    band's conditions were met, or it has no Zero label -- all three fields
    say so instead.
    """

    band_label: str
    text: str
    at: str


@dataclass(frozen=True)
class AnswerCitation:
    """Where the judge's answer quote is, and how exactly it matched (R5).

    Never null and never an error: the quote's provenance was already
    checked, so what's left is pointing a reader at the text. A restated
    quote gets the best-matching line, labelled MATCH_APPROXIMATE, because
    an approximate pointer beats none. coverage is how much of the quote is
    in the answer file, recorded on every grade so the threshold that gates
    it can be set from real runs.
    """

    at: str
    match: str
    coverage: float


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
    condition: Condition
    answer_citation: AnswerCitation


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
    """Return the grade record for one validated reply, carrying the rubric's
    own condition for the awarded band, or the error if it can't be cited.
    """
    LOGGER.debug("build_record(Q%d, repeat %d)", entry.number, repeat)
    condition = _condition(run_files.rubric, entry, judge_reply)
    if isinstance(condition, Exception):
        LOGGER.error("cannot build the record for Q%d, repeat %d", entry.number, repeat)
        return condition
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
        condition=condition,
        answer_citation=_answer_citation(run_files.answer, judge_reply),
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
    return _location_at(path, text, found)


def emit(record: GradeRecord) -> None:
    """Print record to stdout as one JSON line."""
    LOGGER.debug("emit(Q%d, repeat %d)", record.question, record.repeat)
    print(json.dumps(asdict(record), ensure_ascii=False), flush=True)


# PRIVATE FUNCTIONS
def _location_at(path: str, text: str, offset: int) -> str:
    """Return "path:line" for an offset into text."""
    return LOCATION_FORMAT.format(path=path, line=text.count(LINE_BREAK, TEXT_START, offset) + FIRST_LINE)


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


def _condition(
    rubric_file: inputs.InputFile, entry: rubric.RubricEntry, judge_reply: reply.Reply
) -> Condition | Exception:
    """Return the rubric's condition for the awarded band, or the error.

    Nothing to cite -- the judge reported no band's conditions were met, or
    the entry states none for this band -- gives the explicit no-condition
    answer rather than an error: both are real states.
    """
    if reply.is_zero_default(judge_reply.rubric_quote):
        return _no_condition()
    label = _condition_label(judge_reply.band)
    text = rubric.read_band_condition(entry, label)
    if text is None:
        return _no_condition()
    entry_start = max(rubric_file.text.find(entry.text), TEXT_START)
    at = quote_location(rubric_file.path, rubric_file.text, text, entry_start)
    if isinstance(at, Exception):
        return at
    return Condition(band_label=label, text=text, at=at)


def _condition_label(band: str) -> str:
    """Return the label stating band's condition. Every band has one."""
    for known, label in CONDITION_LABELS:
        if band == known:
            return label
    return rubric.LABEL_ZERO


def _no_condition() -> Condition:
    """Return the citation for a band the entry states no condition for."""
    return Condition(band_label=NO_RUBRIC_CONDITION, text=NO_RUBRIC_CONDITION, at=NO_RUBRIC_CONDITION)


def _answer_citation(answer_file: inputs.InputFile, judge_reply: reply.Reply) -> AnswerCitation:
    """Return where the answer quote is and how exactly it matched.

    Tries the quote's own text first; a restated quote falls back to the
    best-matching line rather than to no citation at all.
    """
    if strings.is_empty(judge_reply.answer_quote):
        return AnswerCitation(at=NO_ANSWER_GIVEN, match=NO_ANSWER_GIVEN, coverage=strings.NO_COVERAGE)
    coverage = strings.word_coverage(judge_reply.answer_quote, answer_file.words)
    found = _search_quote(answer_file.text, judge_reply.answer_quote, TEXT_START)
    if found is not None:
        return AnswerCitation(at=_location_at(answer_file.path, answer_file.text, found), match=MATCH_EXACT, coverage=coverage)
    line = _best_matching_line(answer_file.text, judge_reply.answer_quote)
    at = LOCATION_FORMAT.format(path=answer_file.path, line=line)
    return AnswerCitation(at=at, match=MATCH_APPROXIMATE, coverage=coverage)


def _best_matching_line(text: str, quote: str) -> int:
    """Return the line of text sharing the most words with quote.

    Ties go to the earliest line, and a quote sharing nothing with any line
    still returns the first: whether the quote belongs to this file at all
    was already decided before the record was built.
    """
    words = set(strings.normalize_whitespace(quote).split())
    best_line, best_shared = FIRST_LINE, NO_SHARED_WORDS
    for number, line in enumerate(text.splitlines(), start=FIRST_LINE):
        shared = len(words & set(strings.normalize_whitespace(line).split()))
        if shared > best_shared:
            best_line, best_shared = number, shared
    return best_line


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
