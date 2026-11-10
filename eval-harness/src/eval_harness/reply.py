# (C) %COMPANY%
"""The judge model's reply: parsed and validated before anything uses it.

The reply is untrusted (it can echo the answer file). Never log its text:
error messages name the field that failed, not its content.
"""

import json
import logging
import rubric
import strings

from dataclasses import dataclass, fields as dataclass_fields

# CONSTS
LOGGER = logging.getLogger(__name__)
BAND_FULL = "full"
BAND_PARTIAL = "partial"
BAND_ZERO = "zero"
BANDS = frozenset({BAND_FULL, BAND_PARTIAL, BAND_ZERO})
CONFIDENCES = frozenset({"high", "med", "low"})
ZERO_DEFAULT = "Zero - default"
# Which rubric label must exist in the entry for each non-zero band.
BAND_LABELS = ((BAND_FULL, rubric.LABEL_FULL_CREDIT), (BAND_PARTIAL, rubric.LABEL_PARTIAL))
JSON_OBJECT_START = "{"
JSON_OBJECT_END = "}"
NOT_FOUND = -1
# How much of answer_quote must be in the answer file for the quote to have
# come from it. The judge restates what it quotes, so this is well below 1.0;
# a quote sharing less than this was invented. Provisional: no run has been
# measured yet, and every grade records its own coverage so it can be set
# from data rather than from this guess.
MIN_ANSWER_COVERAGE = 0.5
FULL_COVERAGE = 1.0


# TYPES
@dataclass(frozen=True)
class Reply:
    """A validated judge reply. Field order matches the prompt's.

    rubric_quote is kept but not validated. Asking the model to transcribe a
    condition exactly proved past what it does reliably -- it restates them,
    changing a word or a dash -- and failing a grade over that threw away
    sound judgments. It stays in the payload because the prompt's field
    order makes the model write it before it commits to a band, so it reads
    the condition it is about to grade by; and it stays in the record as an
    audit breadcrumb, beside the condition code took from the rubric itself.
    What a band requires is read from the rubric, never from here.
    """

    rubric_quote: str
    answer_quote: str
    reasons: str
    band: str
    confidence: str



# PUBLIC FUNCTIONS
def is_zero_default(rubric_quote: str) -> bool:
    """Return True if rubric_quote is the marker for "no band's conditions
    were met", however its whitespace is spaced.

    This is the one thing read from rubric_quote, and it classifies rather
    than validates: band "zero" alone can't say whether the entry's Zero
    condition was met or no band's conditions were, and those cite different
    things. The marker is three fixed words, which the model does reproduce.
    """
    LOGGER.debug("is_zero_default()")
    return strings.normalize_whitespace(rubric_quote) == ZERO_DEFAULT


def parse_reply(raw: str, entry: rubric.RubricEntry, answer_words: frozenset[str]) -> Reply | Exception:
    """Return the model's raw reply as a validated Reply, or the error.

    Checks the JSON shape and values, that the band exists in the entry,
    that the reasons aren't empty, and that answer_quote is verbatim in the
    answer file (or empty with band zero). rubric_quote is not checked: see
    Reply. answer_words is the answer file's distinct words, computed once
    when it was read: the answer quote is tested against that, not against
    the file's exact characters.
    """
    LOGGER.debug("parse_reply(Q%d, %d chars)", entry.number, len(raw))
    fields = _parse_json_object(raw)
    if isinstance(fields, Exception):
        LOGGER.error("cannot use the reply for Q%d: not a JSON object", entry.number)
        return fields
    reply = _to_reply(fields)
    if isinstance(reply, Exception):
        LOGGER.error("cannot use the reply for Q%d: wrong fields or values", entry.number)
        return reply
    checked = _check_reply(reply, entry, answer_words)
    if isinstance(checked, Exception):
        LOGGER.error("cannot use the reply for Q%d: it failed a check", entry.number)
        return checked
    return reply


# PRIVATE FUNCTIONS
def _parse_json_object(raw: str) -> dict[str, object] | Exception:
    """Return raw parsed as a JSON object, or the error.

    A reply that is only the object parses directly. One wrapped in a code
    fence, or with a sentence before or after it, is retried on the text
    between its outermost braces. The prompt forbids both, but a model that
    adds a wrapper has still answered, and failing the grade over the
    wrapper throws away a sound judgment.
    """
    value = _load_json(raw)
    if isinstance(value, Exception):
        value = _load_json(_between_braces(raw))
    if isinstance(value, Exception):
        return value
    if not isinstance(value, dict):
        return ValueError("reply is JSON but not an object")
    return value


def _load_json(raw: str) -> object | Exception:
    """Return raw parsed as JSON, or the error."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError as err:
        return err


def _between_braces(raw: str) -> str:
    """Return raw from its first { to its last }, or raw unchanged if it has
    no such pair. Whatever comes back is still parsed and validated.
    """
    start = raw.find(JSON_OBJECT_START)
    end = raw.rfind(JSON_OBJECT_END)
    if start == NOT_FOUND or end < start:
        return raw
    return raw[start:end + len(JSON_OBJECT_END)]


def _to_reply(fields: dict[str, object]) -> Reply | Exception:
    """Return fields as a Reply, or the error unless they are exactly Reply's
    fields, all strings, with an allowed band and confidence.
    """
    expected = tuple(field.name for field in dataclass_fields(Reply))
    if set(fields) != set(expected):
        return ValueError(f"reply must have exactly the fields {list(expected)}")
    if not all(isinstance(value, str) for value in fields.values()):
        return ValueError("every reply field must be a string")
    reply = Reply(**fields)
    if reply.band not in BANDS:
        return ValueError(f"band must be one of {sorted(BANDS)}")
    if reply.confidence not in CONFIDENCES:
        return ValueError(f"confidence must be one of {sorted(CONFIDENCES)}")
    return reply


def _check_reply(reply: Reply, entry: rubric.RubricEntry, answer_words: frozenset[str]) -> None | Exception:
    """Return the first failed check on reply, or None.

    Checks run one at a time and stop at the first failure: a later check
    can log (the empty-answer error), so it mustn't run after an earlier fail.
    """
    band = _check_band(reply, entry)
    if isinstance(band, Exception):
        return band
    reasons = _check_reasons(reply, entry)
    if isinstance(reasons, Exception):
        return reasons
    return _check_answer_quote(reply, entry, answer_words)


def _check_reasons(reply: Reply, entry: rubric.RubricEntry) -> None | Exception:
    """Return the error if reply has no reasons. Every grade carries a
    rationale a test engineer can read (R5), so an empty one is not a grade.
    """
    if strings.is_empty(reply.reasons):
        return ValueError(f"reasons is empty for rubric entry Q{entry.number}")
    return None


def _check_band(reply: Reply, entry: rubric.RubricEntry) -> None | Exception:
    """Return the error if reply's band isn't one the entry has. Zero always is."""
    for band, label in BAND_LABELS:
        if reply.band == band and label not in entry.text:
            return ValueError(f"band {band!r} isn't in rubric entry Q{entry.number}")
    return None


def _check_answer_quote(reply: Reply, entry: rubric.RubricEntry, answer_words: frozenset[str]) -> None | Exception:
    """Return the error unless answer_quote came from the answer file, or is
    empty with band zero (no answer: logged as an error, the run continues).

    Came from, not copied from. The judge restates what it quotes, so
    demanding a transcription failed grades that were sound. What must not
    pass is a quote the judge invented: a grade resting on an answer the
    agent never gave is worse than no grade. Coverage separates the two --
    a restated quote keeps nearly all of the answer's words, a fabricated
    one keeps few -- and the report records it for every grade.
    """
    if strings.is_empty(reply.answer_quote):
        if reply.band != BAND_ZERO:
            return ValueError(f"an empty answer_quote is only allowed with band {BAND_ZERO!r}")
        LOGGER.error("Q%d: the judge found no answer and graded zero; check it", entry.number)
        return None
    coverage = strings.word_coverage(reply.answer_quote, answer_words)
    if coverage < MIN_ANSWER_COVERAGE:
        return ValueError(f"answer_quote isn't from the answer file (Q{entry.number}, coverage {coverage:.2f})")
    if coverage < FULL_COVERAGE:
        LOGGER.warning("Q%d: the judge restated the answer it quoted (coverage %.2f)", entry.number, coverage)
    return None
