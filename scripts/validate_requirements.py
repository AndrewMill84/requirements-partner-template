#!/usr/bin/env python3
"""Offline structural checks for this repository's Markdown conventions.

This checks declared records, not business correctness or authentic approval.
See standards/validation.md for the supported Markdown subset and limitations.
"""

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ID = r"(?:FR|BR|EX|D|Q|E)-\d{3,}"
REFERENCE = re.compile(rf"(?:(?P<cap>[a-z0-9][a-z0-9-]*):)?(?P<id>{ID})(?:[–—-](?P<end>{ID}))?\b")
DEFINITION = re.compile(rf"^`?({ID})`?$")
LINK = re.compile(r"\[[^\]\n]*\]\((<[^>]+>|[^\s)]+(?:\([^)]*\)[^\s)]*)*)(?:\s+\"[^\"]*\")?\)")
PLACEHOLDERS = {"", "none", "unknown", "to complete", "to establish", "to record", "not accepted", "not pinned", "not prepared"}
STATUSES = {"draft", "in review", "ready for engineering", "superseded"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str

    def __str__(self):
        return f"{self.path}:{self.line}: {self.code}: {self.message}"


def visible_lines(text):
    """Retain line numbers while excluding fenced examples and HTML comments."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


def fields(lines, header_only=False):
    result = {}
    for _, line in lines:
        if header_only and line.startswith("## "):
            break
        match = re.match(r"^([A-Za-z][A-Za-z /-]+):\s*(.*?)\s*$", line)
        if match:
            result[match[1].lower()] = match[2].strip(" `")
    return result


def references(text, capability):
    for match in REFERENCE.finditer(text):
        namespace = match["cap"] or capability
        first = match["id"]
        if match["end"]:
            prefix, start = first.split("-")
            end_prefix, end = match["end"].split("-")
            if prefix == end_prefix and 0 <= int(end) - int(start) <= 1000:
                for number in range(int(start), int(end) + 1):
                    yield namespace, f"{prefix}-{number:03d}"
                continue
        yield namespace, first
        if match["end"]:
            yield namespace, match["end"]


def rows(lines):
    header = []
    for number, line in lines:
        if not line.lstrip().startswith("|"):
            header = []
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if not header:
            header = [cell.lower() for cell in cells]
        yield number, cells, dict(zip(header, cells))


def heading_anchors(lines):
    counts = defaultdict(int)
    anchors = set()
    for _, line in lines:
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", match[1]).lower()
        slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        candidate = slug
        while candidate in anchors:
            counts[slug] += 1
            candidate = f"{slug}-{counts[slug]}"
        anchors.add(candidate)
    return anchors


def meaningful(value):
    return value.strip(" `").lower() not in PLACEHOLDERS


def validate(root: Path) -> list[Finding]:
    root = root.resolve()
    findings = []
    documents = {}
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part.startswith(".") or part in {"node_modules", "__pycache__"} for part in relative.parts):
            continue
        documents[path] = list(visible_lines(path.read_text(encoding="utf-8")))

    def report(path, line, code, message):
        findings.append(Finding(str(path.relative_to(root)), line, code, message))

    # Local paths and Markdown heading fragments only. Never fetch external sources.
    for path, lines in documents.items():
        for number, line in lines:
            line = re.sub(r"(`+).*?\1", "", line)
            for match in LINK.finditer(line):
                destination = match[1].strip("<>")
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                target = (root / unquote(url.path).lstrip("/") if url.path.startswith("/")
                          else path.parent / unquote(url.path)).resolve() if url.path else path
                if not target.is_relative_to(root) or not target.exists():
                    report(path, number, "broken-link", destination)
                elif url.fragment and target.suffix == ".md":
                    target_lines = documents.get(target)
                    if target_lines is None:
                        target_lines = list(visible_lines(target.read_text(encoding="utf-8")))
                    if unquote(url.fragment) not in heading_anchors(target_lines):
                        report(path, number, "broken-fragment", destination)

    capability_root = root / "capabilities"
    capabilities = sorted(path for path in capability_root.iterdir() if path.is_dir()) if capability_root.exists() else []
    declarations = defaultdict(dict)
    capability_rows = {}
    for folder in capabilities:
        if not (folder / "requirements.md").exists():
            report(folder, 1, "missing-requirements", "Expected requirements.md (compact or multi-file entry point).")
        collected = []
        for path, lines in documents.items():
            if not path.is_relative_to(folder):
                continue
            for number, cells, row in rows(lines):
                collected.append((path, number, cells, row))
                declaration = DEFINITION.fullmatch(cells[0]) if row.get("id") == cells[0] else None
                if declaration:
                    key = declaration[1]
                    if key in declarations[folder.name]:
                        report(path, number, "duplicate-id", f"{key} already declared in {declarations[folder.name][key][0].relative_to(root)}.")
                    else:
                        declarations[folder.name][key] = (path, number)
        capability_rows[folder.name] = collected

    for folder in capabilities:
        for path, number, cells, row in capability_rows[folder.name]:
            # Only an ID column declares a row. Coverage tables contain references.
            declaring = row.get("id") == cells[0] and DEFINITION.fullmatch(cells[0])
            reference_cells = cells[1:] if declaring else cells
            for namespace, key in references(" | ".join(reference_cells), folder.name):
                if key not in declarations[namespace]:
                    report(path, number, "unknown-id", f"{namespace}:{key} has no table declaration.")

        entry = folder / "requirements.md"
        if entry not in documents:
            continue
        meta = fields(documents[entry], header_only=True)
        status = meta.get("status", "").lower()
        if status not in STATUSES:
            report(entry, 1, "status", "Declare Status: Draft, In review, Ready for engineering or Superseded.")
        ready = status == "ready for engineering"
        accepted = set(references(meta.get("accepted scope", ""), folder.name))
        if ready:
            required = ["owner", "accepted by", "accepted on", "accepted scope", "acceptance evidence"]
            missing = [key for key in required if not meaningful(meta.get(key, ""))]
            if missing or meta.get("product acceptance", "").lower() != "accepted":
                report(entry, 1, "readiness", "Explicit acceptance metadata required: " + ", ".join(missing or ["Product acceptance: Accepted"]))
            try:
                raw_date = meta.get("accepted on", "")
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_date):
                    raise ValueError
                date.fromisoformat(raw_date)
            except ValueError:
                report(entry, 1, "readiness", "Accepted on must be a real ISO date (YYYY-MM-DD).")
            if meta.get("material blockers", "").lower() != "none":
                report(entry, 1, "readiness", "Ready scope must declare Material blockers: None.")
            if (not any(key.startswith(("FR-", "BR-")) for _, key in accepted)
                    or not any(key.startswith("EX-") for _, key in accepted)
                    or any(namespace != folder.name or not key.startswith(("FR-", "BR-", "EX-"))
                           or key not in declarations[folder.name]
                           for namespace, key in accepted)):
                report(entry, 1, "readiness", "Accepted scope must contain only declared local FR/BR/EX IDs, including an obligation (FR or BR) and an EX.")
            for path, number, _, row in capability_rows[folder.name]:
                if row.get("status", "").lower() in {"open", "proposed", "unresolved", "deferred"}:
                    blockers = row.get("blocks", "")
                    if blockers.lower() == "all" or accepted.intersection(references(blockers, folder.name)):
                        report(path, number, "readiness", "An unresolved question blocks the accepted scope.")

        # Handoff fields live in implementation.md, or the compact entry's Implementation section.
        handoff_path = folder / "implementation.md"
        if handoff_path not in documents:
            handoff_path = entry
        handoff = fields(documents[handoff_path])
        state = handoff.get("delivery state", "").lower()
        prepared = handoff.get("handoff status", "").lower() == "prepared"
        if prepared or state in {"in progress", "implemented", "verified", "accepted"}:
            if not ready or not prepared:
                report(handoff_path, 1, "handoff", "Delivery requires a Prepared handoff and accepted Ready for engineering scope.")
            baseline = handoff.get("requirements baseline commit sha", "")
            evidence = handoff.get("platform evidence commit sha", "")
            if not re.fullmatch(r"[0-9a-f]{40}", baseline) or not re.fullmatch(r"[0-9a-f]{40}", evidence):
                report(handoff_path, 1, "handoff", "Requirements and platform evidence commits must be full 40-character SHAs.")
            for key in ["pinned requirements link", "pinned decisions link"]:
                link = handoff.get(key, "")
                markdown = LINK.fullmatch(link)
                destination = markdown[1].strip("<>") if markdown else link
                if not re.fullmatch(rf"https://github\.com/[^/\s?#]+/[^/\s?#]+/blob/{re.escape(baseline)}/[^\s)?#]+(?:#[^\s)]+)?", destination):
                    report(handoff_path, 1, "handoff", f"{key} must use the requirements baseline SHA in an immutable GitHub blob URL.")
            included = set(references(handoff.get("included ids", ""), folder.name))
            if (not included or not included.issubset(accepted)
                    or any(not key.startswith(("FR-", "BR-", "EX-")) for _, key in included)
                    or not any(key.startswith(("FR-", "BR-")) for _, key in included)
                    or not any(key.startswith("EX-") for _, key in included)):
                report(handoff_path, 1, "handoff", "Included FR/BR/EX IDs must be within accepted scope and include an obligation and acceptance examples.")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("--root must be an existing repository directory")
    findings = validate(args.root)
    for finding in findings:
        print(finding)
    if not findings:
        print("Structural validation passed. Business correctness and approval authenticity require separate review.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
