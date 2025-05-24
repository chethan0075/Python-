print("Chethan U, 1AY24AI025, SEC-M")
#!/usr/bin/env python3
# TabelPrinter.py

import sys
import csv
import json
from typing import List, Dict, Any


def compute_col_widths(headers: List[str], rows: List[List[Any]]) -> List[int]:
    """Compute maximum width for each column based on headers and row values."""
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    return widths


def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    """Print an ASCII table given headers and row data."""
    if not headers or not rows:
        print("(no data)")
        return

    widths = compute_col_widths(headers, rows)
    # Separator line
    sep = "+".join("-" * (w + 2) for w in widths)
    sep = f"+{sep}+"

    # Header row
    header_cells = [f" {str(h).ljust(widths[i])} " for i, h in enumerate(headers)]
    header_line = "|" + "|".join(header_cells) + "|"

    print(sep)
    print(header_line)
    print(sep.replace('-', '='))  # header separator

    # Data rows
    for row in rows:
        row_cells = [f" {str(cell).ljust(widths[i])} " for i, cell in enumerate(row)]
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def load_csv(path: str, delimiter: str = ",") -> (List[str], List[List[Any]]):
    """Load CSV file into headers and rows."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        all_rows = list(reader)
        if not all_rows:
            return [], []
        headers = all_rows[0]
        data_rows = all_rows[1:]
        return headers, data_rows


def load_json(path: str) -> (List[str], List[List[Any]]):
    """
    Load a JSON file expecting a list of objects (dicts).
    Keys of the first object become headers; missing keys in others are printed blank.
    """
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list) or not data:
        print("JSON must be a non-empty list of objects.")
        sys.exit(1)
    # Determine all keys in the first object (order preserved)
    headers = list(data[0].keys())
    rows = []
    for obj in data:
        row = [obj.get(h, "") for h in headers]
        rows.append(row)
    return headers, rows


def interactive_input() -> (List[str], List[List[Any]]):
    """Prompt user to enter headers and rows manually."""
    headers = input("Enter column headers, comma-separated: ").strip().split(",")
    headers = [h.strip() for h in headers if h.strip()]
    rows: List[List[Any]] = []
    print("Enter rows one by one, comma-separated. Blank line to finish.")
    while True:
        line = input(f"Row {len(rows)+1}: ").strip()
        if not line:
            break
        values = [v.strip() for v in line.split(",")]
        # pad or trim to match headers
        if len(values) < len(headers):
            values += [""] * (len(headers) - len(values))
        elif len(values) > len(headers):
            values = values[:len(headers)]
        rows.append(values)
    return headers, rows


def usage():
    print(f"Usage:")
    print(f"  {sys.argv[0]} path/to/data.csv [delimiter]")
    print(f"  {sys.argv[0]} path/to/data.json")
    print(f"  {sys.argv[0]}           # interactive mode")
    sys.exit(1)


def main():
    if len(sys.argv) == 1:
        # interactive
        headers, rows = interactive_input()
    elif len(sys.argv) == 2:
        path = sys.argv[1]
        if path.lower().endswith(".csv"):
            headers, rows = load_csv(path)
        elif path.lower().endswith(".json"):
            headers, rows = load_json(path)
        else:
            usage()
    elif len(sys.argv) == 3 and sys.argv[1].lower().endswith(".csv"):
        # custom delimiter
        headers, rows = load_csv(sys.argv[1], delimiter=sys.argv[2])
    else:
        usage()

    print_table(headers, rows)


if __name__ == "__main__":
    main()
