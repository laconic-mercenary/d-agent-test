# (C) %COMPANY%
"""Small string helpers shared across the harness."""

import logging
import re

# CONSTS
LOGGER = logging.getLogger(__name__)
WHITESPACE_JOINER = " "
NO_COVERAGE = 0.0


# PUBLIC FUNCTIONS
def trim(value: str) -> str:
    """Return value without leading or trailing whitespace."""
    LOGGER.debug("trim()")
    return value.strip()


def normalize_whitespace(value: str) -> str:
    """Return value with every run of whitespace collapsed to one space, and
    without leading or trailing whitespace.

    Quotes are compared after this, so a hard-wrapped rubric line and the
    same sentence re-flowed onto one line count as the same text. How a file
    is wrapped is formatting, not content.
    """
    LOGGER.debug("normalize_whitespace()")
    return WHITESPACE_JOINER.join(value.split())


def is_empty(value: str | None) -> bool:
    """Return True if value is None, empty, or only whitespace."""
    LOGGER.debug("is_empty()")
    if value is None:
        return True
    return len(trim(value)) == 0


def distinct_words(text: str) -> frozenset[str]:
    """Return the distinct whitespace-separated words of text.

    Computed once per file when it is read, so a quote can be tested against
    it without walking the whole file again on every check.
    """
    LOGGER.debug("distinct_words()")
    return frozenset(normalize_whitespace(text).split())


def word_coverage(quote: str, words: frozenset[str]) -> float:
    """Return the fraction of quote's distinct words that appear in words.

    1.0 means every word of the quote is somewhere in the text it came from;
    0.0 means none is, so the quote wasn't taken from that text at all. This
    is deliberately insensitive to word order and to how either side wraps:
    the judge restates what it quotes, and the question here is provenance,
    not transcription. An empty quote covers nothing.
    """
    LOGGER.debug("word_coverage()")
    quote_words = set(normalize_whitespace(quote).split())
    if not quote_words:
        return NO_COVERAGE
    return len(quote_words & words) / len(quote_words)


def parse_int(text: str) -> int | Exception:
    """Return text parsed as an integer, or the error if it isn't one."""
    LOGGER.debug("parse_int()")
    try:
        return int(text)
    except ValueError as err:
        LOGGER.error("cannot parse text as an integer: %s", err)
        return err


def parse_float(text: str) -> float | Exception:
    """Return text parsed as a float, or the error if it isn't one."""
    LOGGER.debug("parse_float()")
    try:
        return float(text)
    except ValueError as err:
        LOGGER.error("cannot parse text as a number: %s", err)
        return err


def regex_matches(text: str, pattern: re.Pattern[str]) -> bool:
    """Return True if the whole of text matches pattern.

    Uses fullmatch: re.match only anchors at the start, so "abc$" would
    pass a pattern for "abc".
    """
    LOGGER.debug("regex_matches(pattern=%s)", pattern.pattern)
    return pattern.fullmatch(text) is not None
