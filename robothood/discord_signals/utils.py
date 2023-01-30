import re
from typing import List, Union

from robothood.errors import NoMatchFoundError

# pylint:disable=unused-variable


def signal_regex(pattern: str, signal: str) -> Union[str, List[str]]:
    """Extract a pattern from a signal (RegEx Wrapper)

    Parameters
    ----------
    pattern: str
        Regex pattern
    signal: str
        Discord signal as a list of lines

    Raises
    ------
    NoMatchFoundError
        f"Pattern {pattern} not found in {signal}"

    Returns
    -------
    Union[str, List[str]]
        The wanted string matching pattern
    """
    result = re.findall(pattern=pattern, string=signal)
    if len(result) == 0:
        raise NoMatchFoundError(f"Pattern {pattern} not found in {signal}")
    return result[0] if len(result) == 1 else result


def pick_line(signal_list: List[str], keywords: List[str]) -> str:
    """Pick a line that contains keywords in a signal list

    Parameters
    ----------
    signal_list: List[str]
        Discord signal as a list of lines
    keywords: List[str]
        List of keywords expected to be seen in the signal

    Raises
    ------
    NoMatchFoundError
        f"Signal {signal_list} does not contain all the keywords: {keywords}"

    Returns
    -------
    str
        The line containing the keywords
    """
    try:
        return [el for el in signal_list if all([x in el.lower() for x in keywords])][0]
    except IndexError:
        raise NoMatchFoundError(
            f"Signal {signal_list} does not contain all the keywords: {keywords}"
        )
