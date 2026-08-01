"""csv-row-position-shift: rotate CSV data rows by N positions (wrap-around).

Reads from a file argument or stdin when FILE is omitted or "-".
The header row (unless --no-header) stays in place; only data rows rotate.

Exit codes:
    0 success
    1 CLI or I/O error
    2 --check condition not satisfied
"""

import argparse
import csv
import io
import json
import sys


def build_parser():
    p = argparse.ArgumentParser(
        prog="csv-row-position-shift",
        description="Shift CSV data rows by N positions with wrap-around.",
    )
    p.add_argument("file", nargs="?", default="-", help="CSV file (default: stdin)")
    p.add_argument("-n", "--shift", type=int, default=1,
                   help="positions to shift (negative = backwards, default 1)")
    p.add_argument("-d", "--delimiter", default=",", help="field delimiter (default: comma)")
    p.add_argument("--no-header", action="store_true", help="treat the first line as data")
    p.add_argument("--check", metavar="FIRST-KEY", default=None,
                   help="exit 2 unless the first data column of the first row matches FIRST-KEY after shifting")
    p.add_argument("--json", action="store_true", help="print a JSON report instead of the CSV")
    return p


def read_input(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, newline="", encoding="utf-8") as fh:
        return fh.read()


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        text = read_input(args.file)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rows = list(csv.reader(io.StringIO(text), delimiter=args.delimiter))
    if not rows:
        print("error: empty input", file=sys.stderr)
        return 1

    if args.no_header:
        header, data = None, rows
    else:
        header, data = rows[0], rows[1:]

    if data:
        k = args.shift % len(data)
        shifted = data[-k:] + data[:-k] if k else list(data)
    else:
        shifted = []

    ok = True
    if args.check is not None:
        ok = bool(shifted) and shifted[0] and shifted[0][0] == args.check

    report = {
        "file": args.file,
        "shift": args.shift,
        "totalRows": len(data),
        "firstRowKey": shifted[0][0] if shifted and shifted[0] else None,
        "check": args.check,
        "ok": ok,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        out = csv.writer(sys.stdout)
        if header is not None:
            out.writerow(header)
        out.writerows(shifted)

    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
