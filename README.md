# csv-row-position-shift

Rotate CSV data rows by N positions with wrap-around. The header row is
preserved; only data rows move. Negative shifts rotate backwards.

## Features

- Rotate data rows forward or backward (wrap-around)
- Header preserved by default (`--no-header` to treat all rows as data)
- `--check KEY` CI guard: exit 2 unless the first row's key matches after rotation
- `--json` machine-readable report
- Reads stdin when FILE is omitted or `-`

## Install

```bash
pip install .
# or
pip install git+https://github.com/TataneSan/csv-row-position-shift.git
```

## Usage

```bash
printf 'id,name\n1,ann\n2,bob\n3,cid\n' | csv-row-position-shift -n 1
# id,name
# 3,cid
# 1,ann
# 2,bob

printf 'id,name\n1,ann\n2,bob\n3,cid\n' | csv-row-position-shift -n -1
# id,name
# 2,bob
# 3,cid
# 1,ann

# CI guard: fail unless the rotated first row starts with id 3
csv-row-position-shift data.csv -n 1 --check 3

# JSON report
csv-row-position-shift data.csv -n 2 --json
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0    | success (`--check` satisfied when given) |
| 1    | CLI or I/O error |
| 2    | `--check` condition not satisfied |

## License

MIT
