#!/usr/bin/env python3
r"""Bookkeeping of a pattern sweep: every occurrence gets a verdict.

``extract``  list every match of a pattern with an identifier.
``check``    fail unless a verdict table covers each identifier exactly once.

A sweep is a judgment made by an agent; this program only proves that no
occurrence was skipped.  It needs no packages.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

VERDICTS = {"fix", "keep"}


def extract(pattern: str, files: list[str]) -> list[dict]:
    r"""List the matches of a pattern.

    Parameters
    ----------
    pattern : str
        Regular expression, matched line by line.
    files : list of str
        Files to search.

    Returns
    -------
    list of dict
        One row per match with keys ``id``, ``file``, ``line``, ``text``;
        identifiers are ``O001``, ``O002``, ...
    """
    regex = re.compile(pattern)
    rows = []
    for name in files:
        for no, line in enumerate(Path(name).read_text().splitlines(), 1):
            for _ in regex.finditer(line):
                rows.append({"id": f"O{len(rows) + 1:03d}", "file": name, "line": no,
                             "text": line.strip()})
    return rows


def read_table(path: str) -> list[dict]:
    r"""Read a tab-separated table with a header line.

    Parameters
    ----------
    path : str
        File of the table.

    Returns
    -------
    list of dict
        One dict per row, keyed by the header.
    """
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def problems(occurrences: list[dict], verdicts: list[dict]) -> list[str]:
    r"""Compare a verdict table with the list of occurrences.

    Parameters
    ----------
    occurrences : list of dict
        Rows of ``extract``.
    verdicts : list of dict
        Rows with the columns ``id``, ``verdict``, ``reason``.

    Returns
    -------
    list of str
        One message per problem; empty when the table is complete.
    """
    wanted = [row["id"] for row in occurrences]
    seen = [(row.get("id") or "").strip() for row in verdicts]
    out = [f"{i}: no verdict" for i in wanted if i not in seen]
    out += [f"{i}: not an occurrence" for i in dict.fromkeys(seen) if i not in wanted]
    out += [f"{i}: more than one verdict" for i in dict.fromkeys(seen) if seen.count(i) > 1]
    for row in verdicts:
        ident = (row.get("id") or "").strip()
        verdict = (row.get("verdict") or "").strip()
        if verdict not in VERDICTS:
            out.append(f"{ident}: verdict {verdict!r}, expected one of {sorted(VERDICTS)}")
        if not (row.get("reason") or "").strip():
            out.append(f"{ident}: no reason")
    return out


def main(argv: list[str] | None = None) -> int:
    r"""Command-line entry point.

    Parameters
    ----------
    argv : list of str, optional
        Arguments; ``sys.argv[1:]`` if None.

    Returns
    -------
    int
        0 on success, 1 when the verdict table is incomplete.
    """
    top = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = top.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("extract", help="list every match with an identifier")
    p.add_argument("--pattern", required=True, help="regular expression, matched per line")
    p.add_argument("--out", required=True, help="tab-separated file to write")
    p.add_argument("files", nargs="+")
    p = sub.add_parser("check", help="check a verdict table against the occurrences")
    p.add_argument("occurrences")
    p.add_argument("verdicts")
    args = top.parse_args(argv)
    if args.cmd == "extract":
        rows = extract(args.pattern, args.files)
        with open(args.out, "w", newline="") as handle:
            writer = csv.DictWriter(handle, ["id", "file", "line", "text"], delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{len(rows)} occurrences written to {args.out}")
        return 0
    found = problems(read_table(args.occurrences), read_table(args.verdicts))
    for message in found:
        print(message)
    occurrences = read_table(args.occurrences)
    print(f"{len(occurrences)} occurrences, {len(read_table(args.verdicts))} verdict rows, "
          f"{len(found)} problems")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
