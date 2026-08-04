"""Terminal styling for the SAAKSHI demo - standard library only, zero deps.

Colour and Unicode glyphs turn on only for an interactive terminal that can
render them, and turn off automatically when the demo is piped or redirected
(so ``docs/DEMO_OUTPUT.txt`` and any judge piping the run stay clean ASCII) or
when ``NO_COLOR`` is set. Set ``FORCE_COLOR=1`` (or ``CLICOLOR_FORCE=1``) to
force colour on regardless - handy for a recorded screencast.

This module is presentation only. Every number the demo prints is byte-for-byte
identical with or without colour, so Rule R1 (determinism of the citizen-facing
path) is untouched: styling never changes a value, only how it is shown.
"""
from __future__ import annotations

import os
import sys


def _enable_windows_vt() -> None:
    """Best-effort enable of ANSI escape handling on legacy Windows consoles."""
    if os.name != "nt":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:  # pragma: no cover - platform/permission dependent
        pass


def _decide_color() -> bool:
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("FORCE_COLOR") or os.environ.get("CLICOLOR_FORCE"):
        return True
    if os.environ.get("TERM") == "dumb":
        return False
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


def _decide_utf8() -> bool:
    if os.environ.get("SAAKSHI_ASCII"):  # escape hatch for stubborn consoles
        return False
    enc = (getattr(sys.stdout, "encoding", "") or "").lower()
    return "utf" in enc


_enable_windows_vt()
COLOR: bool = _decide_color()
UTF8: bool = _decide_utf8()

RESET = "\x1b[0m"


def _fg(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"


# SAAKSHI palette, in truecolor. Tones are mid-brightness on purpose so they
# read on BOTH dark and light terminal backgrounds (deck navy/cream would
# vanish on one or the other).
_SAFFRON = _fg(0xD9, 0x8A, 0x2B)   # accent / headers  (deck saffron)
_GREEN = _fg(0x3F, 0xB0, 0x6E)     # PASS / VALIDATED
_RED = _fg(0xDD, 0x5B, 0x4E)       # FAIL / no-match
_AMBER = _fg(0xE0, 0xA5, 0x3A)     # ! flags / caveats
_BLUE = _fg(0x3B, 0x8F, 0xC7)      # secondary accent


def _wrap(codes: str, s: str) -> str:
    return f"{codes}{s}{RESET}" if COLOR else s


def bold(s: str) -> str:
    return _wrap("\x1b[1m", s)


def dim(s: str) -> str:
    return _wrap("\x1b[2m", s)


def saffron(s: str) -> str:
    return _wrap(_SAFFRON, s)


def saffron_b(s: str) -> str:
    return _wrap("\x1b[1m" + _SAFFRON, s)


def green(s: str) -> str:
    return _wrap(_GREEN, s)


def green_b(s: str) -> str:
    return _wrap("\x1b[1m" + _GREEN, s)


def red(s: str) -> str:
    return _wrap(_RED, s)


def red_b(s: str) -> str:
    return _wrap("\x1b[1m" + _RED, s)


def amber(s: str) -> str:
    return _wrap(_AMBER, s)


def blue(s: str) -> str:
    return _wrap(_BLUE, s)


# --- glyphs: nicer Unicode when the terminal is UTF-8, ASCII fallback otherwise
HRULE = "═" if UTF8 else "="       # heavy rule  =
HRULE_THIN = "─" if UTF8 else "-"  # thin rule   -
RUPEE = "₹" if UTF8 else "Rs"      # rupee sign  Rs
BULLET = "•" if UTF8 else "."      # bullet      .
ARROW = "→" if UTF8 else "->"      # arrow       ->
BIDIR = "↔" if UTF8 else "<->"     # bidir       <->
LEQ = "≤" if UTF8 else "<="        # less-eq     <=
CHECK = "✓" if UTF8 else ""        # check       (none)
CROSS = "✗" if UTF8 else ""        # cross       (none)


def pass_tag() -> str:
    label = (CHECK + " " if CHECK else "") + "PASS"
    return green_b(label)


def fail_tag() -> str:
    label = (CROSS + " " if CROSS else "") + "FAIL"
    return red_b(label)


def confidence(level: str) -> str:
    """Colour a signal-confidence label by severity."""
    fn = {"HIGH": green_b, "MEDIUM": amber, "LOW": dim, "N/A": dim}.get(level, lambda s: s)
    return fn(f"confidence {level}")
