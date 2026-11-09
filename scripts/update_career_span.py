#!/usr/bin/env python3
"""Update the README career-span block from the month/year dates in the resume.

Experience starts in January 2017. Because the resume does not give a start day,
we calculate completed calendar months and display today's date, not invented
day-level tenure. Timezone is America/New_York.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CAREER_START_YEAR = 2017
CAREER_START_MONTH = 1
START_MARKER = "<!-- CAREER-SPAN:START -->"
END_MARKER = "<!-- CAREER-SPAN:END -->"


def career_span(today):
    months = max(0, (today.year - CAREER_START_YEAR) * 12 + today.month - CAREER_START_MONTH)
    years, remaining_months = divmod(months, 12)
    parts = []
    if years:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if remaining_months or not parts:
        parts.append(f"{remaining_months} month{'s' if remaining_months != 1 else ''}")
    return ", ".join(parts)


def main():
    today = datetime.now(ZoneInfo("America/New_York")).date()
    date_label = f"{today.strftime('%B')} {today.day}, {today.year}"
    block = (
        f"{START_MARKER}\n"
        f"**Career span:** **{career_span(today)}** since **January 2017**"
        f" · updated **{date_label}** (resume records months and years, not exact days).\n"
        f"{END_MARKER}"
    )
    readme = Path(__file__).resolve().parent.parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL)
    if len(pattern.findall(text)) != 1:
        raise SystemExit("Expected exactly one career-span marker pair in README.md")
    updated = pattern.sub(lambda _match: block, text, count=1)
    if updated != text:
        readme.write_text(updated, encoding="utf-8")
        print(f"Updated career span: {career_span(today)}, as of {date_label}")
    else:
        print("README career span is already current")


if __name__ == "__main__":
    main()
