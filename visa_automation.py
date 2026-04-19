#!/usr/bin/env python3
"""Basic visa agency automation script.

Reads applicant records from CSV, assigns simple follow-up actions,
and writes the result to another CSV.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path

REQUIRED_DOCUMENTS = {
    "application_form",
    "passport_copy",
    "photo",
    "financial_proof",
}


def parse_documents(raw_value: str) -> set[str]:
    return {doc.strip().lower() for doc in raw_value.split(";") if doc.strip()}


def determine_action(appointment_date: date, missing_documents: set[str]) -> str:
    if missing_documents:
        return "REQUEST_DOCUMENTS"

    days_until_appointment = (appointment_date - date.today()).days
    if days_until_appointment < 0:
        return "REVIEW_RECORD"
    if days_until_appointment <= 2:
        return "SEND_REMINDER"
    return "NO_ACTION"


def process_applications(input_file: Path, output_file: Path) -> None:
    with input_file.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
            raise ValueError("Input CSV is missing column headers or is empty.")
        records = []

        for row in reader:
            docs = parse_documents(row.get("documents_submitted", ""))
            missing_documents = REQUIRED_DOCUMENTS - docs

            try:
                appointment = datetime.strptime(row["appointment_date"], "%Y-%m-%d").date()
                action = determine_action(appointment, missing_documents)
            except (KeyError, ValueError):
                action = "REVIEW_RECORD"

            records.append(
                {
                    **row,
                    "missing_documents": ";".join(sorted(missing_documents)),
                    "action": action,
                }
            )
        fieldnames = [*reader.fieldnames, "missing_documents", "action"]

    with output_file.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Basic visa agency automation")
    parser.add_argument("input", type=Path, help="Input CSV with visa applicants")
    parser.add_argument("output", type=Path, help="Output CSV with follow-up actions")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    process_applications(args.input, args.output)


if __name__ == "__main__":
    main()
