"""
Compliance Data Validator
A rule-based tool that scans customer/transaction records for the kind of
data-quality and risk issues checked during compliance review — missing
required fields, duplicate ID numbers, and transactions above a reporting
threshold (modeled loosely on BSA/AML-style transaction monitoring).

NOTE: sample_records.csv is synthetic data created for portfolio purposes.

Run:
    python validator.py
"""

import csv
from collections import defaultdict
from datetime import datetime

REQUIRED_FIELDS = ["full_name", "date_of_birth", "id_number", "address"]
HIGH_VALUE_THRESHOLD = 10000.0  # flag transactions at/above this amount for review


def load_records(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def check_missing_fields(record):
    return [field for field in REQUIRED_FIELDS if not record.get(field, "").strip()]


def check_high_value(record):
    try:
        amount = float(record.get("transaction_amount", 0) or 0)
    except ValueError:
        return None
    return amount if amount >= HIGH_VALUE_THRESHOLD else None


def find_duplicate_ids(records):
    seen = defaultdict(list)
    for r in records:
        id_num = r.get("id_number", "").strip()
        if id_num:
            seen[id_num].append(r["record_id"])
    return {k: v for k, v in seen.items() if len(v) > 1}


def validate(records):
    issues = []
    duplicate_ids = find_duplicate_ids(records)
    dup_record_ids = {rid for ids in duplicate_ids.values() for rid in ids}

    for r in records:
        record_issues = []

        missing = check_missing_fields(r)
        if missing:
            record_issues.append(f"Missing required field(s): {', '.join(missing)}")

        high_value = check_high_value(r)
        if high_value is not None:
            record_issues.append(f"High-value transaction (${high_value:,.2f}) — flagged for review")

        if r["record_id"] in dup_record_ids:
            record_issues.append(f"Duplicate ID number ({r['id_number']}) shared with another record")

        if record_issues:
            issues.append({"record_id": r["record_id"], "issues": record_issues})

    return issues, duplicate_ids


def write_report(issues, out_path="validation_report.csv"):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["record_id", "issue"])
        for entry in issues:
            for issue in entry["issues"]:
                writer.writerow([entry["record_id"], issue])


def main():
    records = load_records("sample_records.csv")
    issues, duplicate_ids = validate(records)
    write_report(issues)

    print(f"Validated {len(records)} records.")
    print(f"{len(issues)} record(s) flagged with at least one issue.\n")

    for entry in issues:
        print(f"[{entry['record_id']}]")
        for issue in entry["issues"]:
            print(f"   - {issue}")

    print(f"\nFull report written to validation_report.csv")


if __name__ == "__main__":
    main()
