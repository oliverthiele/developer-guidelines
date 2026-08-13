#!/usr/bin/env python3
"""Find changelog entries that the guidelines should react to.

Compares the guideline files against the changelog index and ranks entries that
touch something the guidelines already talk about, but do not cite.

The point is not to find candidates — that is easy and useless, because 800
entries face roughly a dozen citations. The point is to only ever show what has
not been judged yet: every entry is either cited by a guideline, recorded in
reviewed.tsv, or shown. An audit without that memory reports hundreds of
candidates once and is ignored from then on.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

CITATION_PATTERN = re.compile(r"#(\d{5,6})\b")
CODE_TOKEN_PATTERN = re.compile(r"`([^`]+)`")
IDENTIFIER_PATTERN = re.compile(r"\b([A-Z][a-z]+(?:[A-Z][a-z]*)+)\b")
WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_:.-]{3,}")

TYPE_WEIGHT = {"Breaking": 4, "Important": 4, "Deprecation": 3, "Feature": 1}

# Words that appear in nearly every changelog title and every guideline, and
# therefore carry no signal.
STOPWORDS = {
    "typo3", "with", "from", "that", "this", "into", "when", "used", "using",
    "which", "have", "been", "will", "must", "should", "code", "file", "files",
    "class", "classes", "method", "methods", "value", "values", "field",
    "fields", "type", "types", "name", "names", "option", "options", "support",
    "backend", "frontend", "core", "extension", "extensions", "configuration",
    "introduce", "introduced", "improved", "removed", "deprecated", "added",
    "allow", "allows", "make", "makes", "based", "default", "defaults", "more",
    "less", "also", "only", "instead", "usage", "rendering", "handling",
}

MIN_SCORE = 8
# A title word occurring in more than this share of all changelog entries
# describes the corpus, not the entry. Cheaper and more honest than growing the
# stopword list forever.
MAX_TOKEN_SHARE = 0.02


def all_markdown(guidelines_dir):
    for path in sorted(guidelines_dir.rglob("*.md")):
        if "changelog-index" not in path.parts:
            yield path


def matchable_files(guidelines_dir):
    """Files a TYPO3 changelog entry could ever ask to change.

    Index files (README.md, versions.md) list topics rather than stating them,
    so every term in them matches something — they would dominate the ranking
    while never being the file that needs changing. Files outside the TYPO3 and
    XLIFF areas cannot be affected by a TYPO3 changelog at all.
    """
    for path in all_markdown(guidelines_dir):
        if path.name in ("README.md", "versions.md"):
            continue
        relative = path.relative_to(guidelines_dir)
        if relative.parts[0] not in ("typo3", "xliff"):
            continue
        yield path


def guideline_terms(text):
    """Distinctive tokens a guideline talks about.

    Two kinds, weighted differently by the caller: code tokens and identifiers
    (strong — a class name in a guideline is a real subject), and prose words
    (weaker, but the signal that catches non-PHP topics such as XLIFF
    whitespace).
    """
    strong = set()
    for match in CODE_TOKEN_PATTERN.finditer(text):
        for identifier in IDENTIFIER_PATTERN.findall(match.group(1)):
            strong.add(identifier.lower())
        cleaned = match.group(1).strip().strip("<>`\\")
        if 3 < len(cleaned) < 40 and " " not in cleaned:
            strong.add(cleaned.lower())
    for identifier in IDENTIFIER_PATTERN.findall(text):
        strong.add(identifier.lower())

    weak = {
        word.lower()
        for word in WORD_PATTERN.findall(text)
        if word.lower() not in STOPWORDS
    }
    return strong, weak - strong


def load_index(index_dir):
    rows = []
    for tsv in sorted(index_dir.glob("v*.tsv")):
        for line in tsv.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 10:
                continue
            rows.append(
                {
                    "number": parts[0],
                    "type": parts[1],
                    "version": parts[2],
                    "title": parts[3],
                    "tags": parts[4].split(),
                    "symbols": parts[5].split(),
                    "gist": parts[6],
                    "path": parts[9],
                }
            )
    return rows


def load_reviewed(index_dir):
    reviewed = {}
    path = index_dir / "reviewed.tsv"
    if not path.is_file():
        return reviewed
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            reviewed[parts[0].strip()] = parts[1].strip()
    return reviewed


def title_tokens(title):
    return {
        word.lower()
        for word in WORD_PATTERN.findall(title)
        if word.lower() not in STOPWORDS
    }


def common_tokens(rows):
    """Title words too frequent across the index to carry signal."""
    counts = defaultdict(int)
    for entry in rows:
        for token in title_tokens(entry["title"]):
            counts[token] += 1
    threshold = max(3, int(len(rows) * MAX_TOKEN_SHARE))
    return {token for token, count in counts.items() if count > threshold}


def score_entry(entry, guidelines, common):
    """Best-matching guideline file and its score."""
    best_file, best_score, best_reason = None, 0, []
    entry_symbols = {symbol.lower().rstrip("()") for symbol in entry["symbols"]}
    tokens = title_tokens(entry["title"]) - common

    for path, (strong, weak) in guidelines.items():
        symbol_hits = entry_symbols & strong
        token_hits = tokens & (strong | weak)
        if not symbol_hits and not token_hits:
            continue
        score = 4 * len(symbol_hits) + len(token_hits) + TYPE_WEIGHT.get(entry["type"], 1)
        if score > best_score:
            reason = []
            if symbol_hits:
                reason.append("symbols: " + ", ".join(sorted(symbol_hits)[:4]))
            if token_hits:
                reason.append("terms: " + ", ".join(sorted(token_hits)[:4]))
            best_file, best_score, best_reason = path, score, reason
    return best_file, best_score, best_reason


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guidelines", default="guidelines", help="guidelines directory")
    parser.add_argument("--limit", type=int, default=15, help="how many candidates to show")
    parser.add_argument(
        "--min-score", type=int, default=MIN_SCORE, help="ignore weaker matches"
    )
    parser.add_argument(
        "--show-reviewed", action="store_true", help="also list what was already judged"
    )
    arguments = parser.parse_args()

    guidelines_dir = Path(arguments.guidelines).expanduser().resolve()
    if not guidelines_dir.is_dir():
        sys.exit(f"guidelines directory not found: {guidelines_dir}")
    index_dir = guidelines_dir / "typo3" / "changelog-index"

    # Citations count from every file — versions.md is where most of them live —
    # while only rule and practice files are matched against.
    cited = set()
    for path in all_markdown(guidelines_dir):
        cited.update(CITATION_PATTERN.findall(path.read_text(encoding="utf-8", errors="replace")))

    guidelines = {}
    for path in matchable_files(guidelines_dir):
        text = path.read_text(encoding="utf-8", errors="replace")
        guidelines[path.relative_to(guidelines_dir)] = guideline_terms(text)

    reviewed = load_reviewed(index_dir)
    rows = load_index(index_dir)
    common = common_tokens(rows)

    print(f"guidelines: {len(guidelines)} files, {len(cited)} changelog entries cited")
    print(f"index: {len(rows)} entries, {len(reviewed)} already judged\n")

    candidates = []
    for entry in rows:
        if entry["number"] in cited or entry["number"] in reviewed:
            continue
        path, score, reason = score_entry(entry, guidelines, common)
        if path is not None and score >= arguments.min_score:
            candidates.append((score, entry, path, reason))

    candidates.sort(key=lambda item: (-item[0], item[1]["number"]))

    grouped = defaultdict(list)
    for score, entry, path, reason in candidates[: arguments.limit]:
        grouped[path].append((score, entry, reason))

    if not grouped:
        print("No unjudged candidates above the threshold.")
    for path, items in grouped.items():
        print(f"→ {path}")
        for score, entry, reason in items:
            print(
                f"   [{score:>3}] #{entry['number']} {entry['type']} {entry['version']} "
                f"— {entry['title']}"
            )
            print(f"         {'; '.join(reason)}")
            if entry["gist"]:
                print(f"         {entry['gist'][:110]}")
        print()

    remaining = len(candidates) - min(len(candidates), arguments.limit)
    if remaining:
        print(f"({remaining} further candidates above the threshold, not shown)")

    print(
        "\nRecord a verdict for everything shown, in "
        "guidelines/typo3/changelog-index/reviewed.tsv:\n"
        "  <number>\\t<covered|not-relevant|todo>\\t<note>\n"
        "Entries cited by a guideline count as covered automatically."
    )

    if arguments.show_reviewed and reviewed:
        print("\nAlready judged:")
        for number, verdict in sorted(reviewed.items()):
            print(f"  #{number}: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
