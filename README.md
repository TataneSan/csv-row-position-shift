# csv-row-position-shift

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

Shift (rotate) the data rows of a CSV file by N positions, with wrap-around. Positive N moves rows down (the last rows come first); negative N moves them up. The header row is preserved unless `--no-header` is given.

## Features

- Shift by any integer - wraps around modulo the row count
- Negative shifts supported (rotate the other way)
- Header preserved by default, `--no-header` available
- `--check` CI mode: exit 2 when rows are not already in the shifted order
- `--json` machine-readable report

## Installation

```bash
pip install .
# or directly from the repo
pip install git+https://github.com/TataneSan/csv-row-position-shift.git
```

## Usage

```
csv-row-position-shift data.csv --shift 1
cat data.csv | csv-row-position-shift --shift -2
csv-row-position-shift data.csv --shift 1 --check
```

### Example

Input `queue.csv`:

```
task,prio
a,1
b,2
c,3
```

```
$ csv-row-position-shift queue.csv --shift 1
task,prio
c,3
a,1
b,2

$ csv-row-position-shift queue.csv --shift -1
task,prio
b,2
c,3
a,1

$ csv-row-position-shift queue.csv --shift 1 --check
rows are not in the requested shifted order
$ echo $?
2
```

## Exit codes

- `0` - success
- `1` - I/O or CLI error
- `2` - `--check` failed: rows not in the shifted order

## License

MIT - see [LICENSE](LICENSE).
