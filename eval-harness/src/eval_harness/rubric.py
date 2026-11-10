# (C) %COMPANY%
"""A case's rubric (grading_schema.md), split into validated entries."""

import logging
import re
import strings

from dataclasses import dataclass

# CONSTS
LOGGER = logging.getLogger(__name__)
SECTION_SEPARATOR = "##"
FIRST_SECTION_INDEX = 1  # index 0 is the preamble before the first "##"
LINE_BREAK = "\n"
# .match is intended here: it checks the heading *starts* with Q<n>.
QUESTION_PATTERN = re.compile(r"Q(\d+)")
POINTS_PATTERN = re.compile(r"\((\d{1,2}) pts\)")
FIRST_CAPTURE_GROUP = 1  # the single (\d+) group in QUESTION_PATTERN and POINTS_PATTERN
LABEL_EXPECTED = "**Expected:**"
LABEL_FULL_CREDIT = "**Full credit:**"
LABEL_PARTIAL = "**Partial:**"
LABEL_ZERO = "**Zero:**"
# Every label an entry can hold, in the order entries use them. A condition
# runs from its own label to whichever of these comes next.
CONDITION_LABELS = (LABEL_EXPECTED, LABEL_FULL_CREDIT, LABEL_PARTIAL, LABEL_ZERO)
LABEL_NOT_FOUND = -1


# TYPES
@dataclass(frozen=True)
class RubricEntry:
    """One `## Q<n>` section of a rubric.

    text is the whole section, heading line included: it's what the judge
    receives for this question, and what read_band_condition slices a
    band's condition out of. It stays exactly as authored, because the
    prompt and the report's line lookup both need the original wrapping.
    """

    number: int
    points: int
    heading: str
    text: str


# PUBLIC FUNCTIONS
def read_rubric_entries_as_list(rubric_text: str) -> tuple[RubricEntry, ...] | Exception:
    """Return the rubric's entries in order, or the first error.

    The rubric is split naively on "##"; the preamble before the first one is
    dropped. Fails if an entry is malformed, or if there are no entries.
    """
    LOGGER.debug("read_rubric_entries_as_list(%d chars)", len(rubric_text))
    entries = []
    for section in _split_sections(rubric_text):
        entry = _parse_entry(section)
        if isinstance(entry, Exception):
            LOGGER.error("cannot read rubric entries")
            return entry
        entries.append(entry)
    if not entries:
        LOGGER.error("cannot read rubric entries: none found")
        return ValueError("no rubric entries found")
    return tuple(entries)


def read_band_condition(entry: RubricEntry, label: str) -> str | None:
    """Return entry's condition for label, the label included, or None if the
    entry doesn't state one.

    The condition runs from its own label to the next label in the entry, so
    what comes back is the text the rubric states for that band and nothing
    else. This is the authority on what a band requires: the judge's own
    quote of it is never used for the record (R5).
    """
    LOGGER.debug("read_band_condition(Q%d, %s)", entry.number, label)
    start = entry.text.find(label)
    if start == LABEL_NOT_FOUND:
        return None
    return strings.trim(entry.text[start:_next_label_at(entry.text, start)])


# PRIVATE FUNCTIONS
def _next_label_at(text: str, start: int) -> int:
    """Return where the first label after start begins, or the end of text."""
    found = [text.find(label, start + 1) for label in CONDITION_LABELS]
    return min([at for at in found if at > LABEL_NOT_FOUND] + [len(text)])


def _split_sections(rubric_text: str) -> tuple[str, ...]:
    """Return each section after a "##", trimmed, in order. The preamble is dropped."""
    sections = rubric_text.split(SECTION_SEPARATOR)[FIRST_SECTION_INDEX:]
    return tuple(strings.trim(section) for section in sections)


def _parse_entry(section: str) -> RubricEntry | Exception:
    """Return the section as a RubricEntry, or the error.

    The heading must start with Q<n> and contain "(<n> pts)" (one or two
    digits). The labels must pass _check_labels.
    """
    heading = section.partition(LINE_BREAK)[0]
    number = QUESTION_PATTERN.match(heading)
    if number is None:
        LOGGER.error("cannot parse rubric entry %r: heading doesn't start with Q<n>", heading)
        return ValueError(f"rubric heading doesn't start with Q<n>: {heading!r}")
    points = POINTS_PATTERN.search(heading)
    if points is None:
        LOGGER.error("cannot parse rubric entry %r: heading has no (<n> pts)", heading)
        return ValueError(f"rubric heading has no (<n> pts): {heading!r}")
    labels = _check_labels(section, heading)
    if isinstance(labels, Exception):
        return labels
    return RubricEntry(
        number=int(number.group(FIRST_CAPTURE_GROUP)),
        points=int(points.group(FIRST_CAPTURE_GROUP)),
        heading=heading,
        text=section,
    )


def _check_labels(section: str, heading: str) -> None | Exception:
    """Return the error if the section has neither a Full credit nor a Zero
    label. Logs a warning, but carries on, if it has no Expected label.
    """
    if LABEL_FULL_CREDIT not in section and LABEL_ZERO not in section:
        LOGGER.error("cannot use rubric entry %r: it has neither %s nor %s", heading, LABEL_FULL_CREDIT, LABEL_ZERO)
        return ValueError(f"rubric entry has neither {LABEL_FULL_CREDIT} nor {LABEL_ZERO}: {heading!r}")
    if LABEL_EXPECTED not in section:
        LOGGER.warning("rubric entry %r has no %s label", heading, LABEL_EXPECTED)
    return None
