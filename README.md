# Compliance Data Validator

🔗 **Live Demo:** [compliance-validator demo](https://apega-tech.github.io/compliance-validator/) — paste your own CSV and validate it live in the browser

A rule-based Python tool that scans customer/transaction records for
data-quality and risk issues — missing required fields, duplicate ID
numbers, and transactions above a reporting threshold. Inspired by the
manual review work done in BSA/AML and KYC compliance roles, rebuilt as
an automated check.

**Note:** `sample_records.csv` is synthetic data created for the portfolio
purposes — it does not contain real customer information.

## Stack
- Python (standard library only — `csv`, `collections`)

## What it checks
- **Missing required fields** — full name, date of birth, ID number, address
- **Duplicate ID numbers** — the same ID number appearing across multiple records
- **High-value transactions** — transactions at or above a $10,000 threshold, flagged for review (a simplified version of real reporting thresholds used in transaction monitoring)

## Run it locally
```bash
python validator.py
```
This prints a summary to the console and writes a full breakdown to
`validation_report.csv`.

## Why this project
At PLS Check Cashers, I manually reviewed identity documents and
transaction data for 100+ customers a day to catch exactly these kinds
of issues — missing information, duplicate records, and transactions
that needed extra scrutiny. This project automates that same logic,
turning a manual compliance workflow into a reusable script.

## Possible next steps
- Add a simple HTML report output instead of CSV
- Make thresholds and required fields configurable via a config file
- Add unit tests for each validation rule
