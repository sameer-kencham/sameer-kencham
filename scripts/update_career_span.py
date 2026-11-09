#!/usr/bin/env python3
"""Refresh the GitHub profile's calendar-accurate career-span display.

The assumed start day (2017-01-10) was provided as an estimate, not a verified
employment record. Role dates in the resume are only recorded by month/year.
The displayed date uses America/New_York.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ESTIMATED_CAREER_START = date(2017, 1, 10)
START_MARKER = "<!-- CAREER-SPAN:START -->"
END_MARKER = "<!-- CAREER-SPAN:END -->"


def career_span(today: date) -> str:
    if today < ESTIMATED_CAREER_START:
        return "0 years, 0 months, 0 days"
    total_months = (
        (today.year - ESTIMATED_CAREER_START.year) * 12
        + today.month - ESTIMATED_CAREER_START.month
    )
    if today.day < ESTIMATED_CAREER_START.day:
        total_months -= 1
    years, months = divmod(total_months, 12)
    anniversary = date(
        ESTIMATED_CAREER_START.year + total_months // 12,
        (ESTIMATED_CAREER_START.month - 1 + total_months) % 12 + 1,
        ESTIMATED_CAREER_START.day,
    )
    days = (today - anniversary).days
    return (
        f"{years} year{'s' if years != 1 else ''}, "
        f"{months} month{'s' if months != 1 else ''}, "
        f"{days} day{'s' if days != 1 else ''}"
    )


def main() -> None:
    today = datetime.now(ZoneInfo("America/New_York")).date()
    date_label = f"{today.strftime('%B')} {today.day}, {today.year}"
    block = (
        f"{START_MARKER}\n"
        f"**Career span:** **{career_span(today)}**"
        f" · estimated start **January 10, 2017**"
        f" · updated **{date_label}**"
        f" (start day is an estimate, not a verified employment record).\n"
        f"{END_MARKER}"
    )
    readme = Path(__file__).resolve().parent.parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    if len(pattern.findall(text)) != 1:
        raise SystemExit("Expected exactly one career-span marker pair in README.md")
    updated = pattern.sub(lambda _: block, text, count=1)
    if updated != text:
        readme.write_text(updated, encoding="utf-8")
        print(f"Updated career span: {career_span(today)} (as of {date_label})")
    else:
        print("README career span is already current")


if __name__ == "__main__":
    main()
