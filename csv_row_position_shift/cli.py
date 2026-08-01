"""csv_row_position_shift - rotate CSV rows by N positions with wrap-around.

Exit codes:
    0 - success
    1 - I/O or CLI error
    2 - --check failed (rows are not in the requested shifted order)
"""
import argparse
import csv
import json
import sys


def _open(path):
    if path in (None, "-"):
        return sys.stdin
    return open(path, newline="", encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="csv-row-position-shift",
        description="Shift (rotate) the data rows of a CSV by N positions with wrap-around.")
    p.add_argument("csv", nargs="?", default="-", help="CSV file (default: stdin)")
    p.add_argument("--shift", type=int, required=True,
                   help="positions to shift (positive moves down, negative moves up)")
    p.add_argument("--no-header", action="store_true", help="input has no header row")
    p.add_argument("--check", action="store_true",
                   help="exit 2 if rows are not already in the shifted order")
    p.add_argument("--json", action="store_true", help="report as JSON")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="suppress transformed output in --check mode")
    args = p.parse_args(argv)

    with _open(args.csv) as fh:
        rows = list(csv.reader(fh))
    if not rows:
        print("error: empty CSV", file=sys.stderr)
        return 1

    if args.no_header:
        header, data = None, rows
    else:
        header, data = rows[0], rows[1:]

    n = len(data)
    shift = args.shift % n if n else 0
    shifted = data[-shift:] + data[:-shift] if shift else list(data)
    already = shifted == data

    report = {"ok": already, "rows": n, "shift": args.shift,
              "effective_shift": shift}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    if args.check:
        if already:
            return 0
        if not args.json:
            print("rows are not in the requested shifted order", file=sys.stderr)
        return 2

    if not args.quiet:
        w = csv.writer(sys.stdout)
        if header is not None:
            w.writerow(header)
        for row in shifted:
            w.writerow(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
