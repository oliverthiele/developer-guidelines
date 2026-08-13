#!/usr/bin/env python3
"""Build a grep-optimised index of TYPO3 changelog entries.

Reads the reStructuredText changelog files shipped with the TYPO3 core
(``vendor/typo3/cms-core/Documentation/Changelog/``) and writes one TSV line
per entry. The index is meant to be searched with ``grep``, never read as a
whole.

See SKILL.md for the workflow and the column contract.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CORE_REPOSITORY = "TYPO3/typo3"
CORE_CHANGELOG_PATH = "typo3/sysext/core/Documentation/Changelog"
# Fetching bodies costs one request per entry. Above this count the index is
# built from file names alone and bodies are filled in on demand instead.
REMOTE_BODY_LIMIT = 150

ENTRY_TYPES = ("Breaking", "Deprecation", "Feature")

# Documentation/Changelog/{version}/{Type}-{number}-{Title}.rst
FILE_PATTERN = re.compile(r"^(Breaking|Deprecation|Feature|Important)-(\d+)-(.+)\.rst$")
VERSION_DIR_PATTERN = re.compile(r"^(\d+)\.(\d+)(\.x)?$")

# "Breaking: #101292 - Strong-typed PropertyMappingConfigurationInterface"
HEADING_PATTERN = re.compile(r"^(?:Breaking|Deprecation|Feature|Important):\s*#(\d+)\s*-\s*(.+)$")

# :php:`\TYPO3\CMS\Fluid\View\StandaloneView` / :php-short:`\TYPO3\...`
PHP_ROLE_PATTERN = re.compile(r":php(?:-short)?:`([^`]+)`")
# Any remaining rst role, e.g. :ref:`foo <bar>` or :issue:`104773`
ANY_ROLE_PATTERN = re.compile(r":[a-z-]+:`([^`]+)`")
LITERAL_PATTERN = re.compile(r"``([^`]+)``")

SECTION_UNDERLINE_PATTERN = re.compile(r"^[=\-~^\"']{3,}\s*$")
INDEX_DIRECTIVE_PATTERN = re.compile(r"^\.\.\s+index::\s*(.+)$")

GIST_MAX_LENGTH = 200
# Catch-all entries such as "Deprecated functionality removed" mention hundreds
# of symbols. An uncapped list would make a single grep hit cost more than
# reading the source file — the opposite of what this index is for.
MAX_SYMBOLS = 30

# Trailing link target of a cross-reference role: :ref:`Title <anchor>`.
# Anchored at the end so role content that legitimately starts with "<"
# (e.g. :typoscript:`<INCLUDE_TYPOSCRIPT:`) survives intact.
ROLE_TARGET_PATTERN = re.compile(r"\s*<[^<>]*>$")


def read_sections(lines):
    """Split an rst document into {section title: body text}."""
    sections = {}
    current_title = None
    current_body = []
    for index, line in enumerate(lines):
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        is_heading = (
            line.strip()
            and SECTION_UNDERLINE_PATTERN.match(next_line)
            and len(next_line.strip()) >= len(line.strip())
        )
        if is_heading:
            if current_title is not None:
                sections[current_title] = "\n".join(current_body).strip()
            current_title = line.strip()
            current_body = []
        elif SECTION_UNDERLINE_PATTERN.match(line) and current_body == []:
            continue  # underline of the heading we just consumed
        elif current_title is not None:
            current_body.append(line)
    if current_title is not None:
        sections[current_title] = "\n".join(current_body).strip()
    return sections


def short_name(fully_qualified):
    """\\TYPO3\\CMS\\Fluid\\View\\StandaloneView -> StandaloneView"""
    name = fully_qualified.strip().lstrip("\\")
    name = name.split("::")[-1] if "::" in name else name.split("\\")[-1]
    return name.strip()


def collect_symbols(text):
    """Short class/method names mentioned in the entry.

    The ExtensionScanner and PHPStan report short names, so those are what a
    lookup will be started from.
    """
    symbols = []
    for match in PHP_ROLE_PATTERN.finditer(text):
        name = short_name(match.group(1))
        if name and name not in symbols:
            symbols.append(name)
    if len(symbols) > MAX_SYMBOLS:
        return symbols[:MAX_SYMBOLS] + [f"+{len(symbols) - MAX_SYMBOLS}-more-see-rst"]
    return symbols


def strip_markup(text):
    """Turn rst prose into a single readable line."""
    text = PHP_ROLE_PATTERN.sub(lambda match: short_name(match.group(1)), text)
    text = ANY_ROLE_PATTERN.sub(
        lambda match: ROLE_TARGET_PATTERN.sub("", match.group(1)).strip(), text
    )
    text = LITERAL_PATTERN.sub(lambda match: match.group(1), text)
    text = re.sub(r"^\.\.\s+.*$", "", text, flags=re.MULTILINE)  # directives
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_gist(sections):
    """One-line migration hint, extracted from Migration (fallback: Impact).

    Lossy by construction — the column is a pointer, not the authority.
    """
    for section in ("Migration", "Impact", "Description"):
        body = sections.get(section, "")
        if not body:
            continue
        # Skip code blocks; prose before the first block is the summary.
        prose = body.split("..  code-block")[0].split(".. code-block")[0]
        gist = strip_markup(prose)
        if not gist:
            continue
        if len(gist) > GIST_MAX_LENGTH:
            cut = gist.rfind(". ", 0, GIST_MAX_LENGTH)
            gist = gist[: cut + 1] if cut > 60 else gist[:GIST_MAX_LENGTH].rstrip() + "…"
        return gist
    return ""


def collect_tags(lines):
    """Categories from the trailing `.. index::` directive (PHP-API, TCA, ...)."""
    for line in reversed(lines):
        match = INDEX_DIRECTIVE_PATTERN.match(line.strip())
        if match:
            tags = [tag.strip() for tag in match.group(1).split(",") if tag.strip()]
            return tags
    return []


def parse_entry(path, version):
    match = FILE_PATTERN.match(path.name)
    if not match:
        return None
    entry_type, number, _ = match.groups()
    if entry_type not in ENTRY_TYPES:
        return None

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    title = ""
    for line in lines:
        heading = HEADING_PATTERN.match(line.strip())
        if heading:
            title = heading.group(2).strip()
            break
    if not title:
        title = re.sub(r"(?<!^)(?=[A-Z])", " ", match.group(3)).strip()

    sections = read_sections(lines)
    return {
        "number": number,
        "type": entry_type,
        "version": version,
        "title": title,
        "tags": collect_tags(lines),
        "symbols": collect_symbols(text),
        "gist": build_gist(sections),
        "path": f"{version}/{path.name}",
    }


def harvest_local(changelog_dir, major):
    entries = []
    for version_dir in sorted(changelog_dir.iterdir()):
        if not version_dir.is_dir():
            continue
        version_match = VERSION_DIR_PATTERN.match(version_dir.name)
        if not version_match or version_match.group(1) != str(major):
            continue
        for rst_file in sorted(version_dir.glob("*.rst")):
            entry = parse_entry(rst_file, version_dir.name)
            if entry:
                entries.append(entry)
    return entries


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "typo3-changelog-harvest"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": "typo3-changelog-harvest"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_entry_text(text, file_name, version):
    """Same extraction as parse_entry(), but for content already in memory."""
    match = FILE_PATTERN.match(file_name)
    if not match or match.group(1) not in ENTRY_TYPES:
        return None
    entry_type, number, camel_title = match.groups()

    lines = text.splitlines() if text else []
    title = ""
    for line in lines:
        heading = HEADING_PATTERN.match(line.strip())
        if heading:
            title = heading.group(2).strip()
            break
    if not title:
        title = re.sub(r"(?<!^)(?=[A-Z])", " ", camel_title).strip()

    sections = read_sections(lines) if lines else {}
    return {
        "number": number,
        "type": entry_type,
        "version": version,
        "title": title,
        "tags": collect_tags(lines),
        "symbols": collect_symbols(text) if text else [],
        "gist": build_gist(sections) if sections else "",
        "path": f"{version}/{file_name}",
    }


def harvest_remote(major, branch, cache_dir):
    """Index a version that is not installed locally (e.g. v15 while on v14).

    The file name already carries type, number and title, so the directory
    listing alone yields a usable index. Bodies are only fetched while the
    entry count stays small; beyond that they are filled in on demand.
    """
    listing_url = (
        f"https://api.github.com/repos/{CORE_REPOSITORY}/contents/"
        f"{CORE_CHANGELOG_PATH}?ref={branch}"
    )
    version_dirs = []
    for item in fetch_json(listing_url):
        if item.get("type") != "dir":
            continue
        version_match = VERSION_DIR_PATTERN.match(item["name"])
        if version_match and version_match.group(1) == str(major):
            version_dirs.append(item["name"])

    file_names = []
    for version in sorted(version_dirs):
        directory_url = (
            f"https://api.github.com/repos/{CORE_REPOSITORY}/contents/"
            f"{CORE_CHANGELOG_PATH}/{version}?ref={branch}"
        )
        for item in fetch_json(directory_url):
            if item.get("type") == "file" and item["name"].endswith(".rst"):
                file_names.append((version, item["name"]))

    fetch_bodies = len(file_names) <= REMOTE_BODY_LIMIT
    if not fetch_bodies:
        print(
            f"v{major}: {len(file_names)} entries — indexing from file names only, "
            "bodies stay unfetched (grep still finds number, type, version, title).",
            file=sys.stderr,
        )

    entries = []
    for version, file_name in file_names:
        text = ""
        if fetch_bodies and FILE_PATTERN.match(file_name):
            cached = cache_dir / version / file_name
            if cached.exists():
                text = cached.read_text(encoding="utf-8", errors="replace")
            else:
                raw_url = (
                    f"https://raw.githubusercontent.com/{CORE_REPOSITORY}/{branch}/"
                    f"{CORE_CHANGELOG_PATH}/{version}/{file_name}"
                )
                text = fetch_text(raw_url)
                cached.parent.mkdir(parents=True, exist_ok=True)
                cached.write_text(text, encoding="utf-8")
        entry = parse_entry_text(text, file_name, version)
        if entry:
            entries.append(entry)
    return entries


def detect_source(changelog_dir):
    """Provenance label from the highest version directory present.

    The changelog folder only ever contains versions up to the installed core,
    so its highest entry identifies which core produced this index.
    """
    versions = []
    for entry in changelog_dir.iterdir():
        match = VERSION_DIR_PATTERN.match(entry.name) if entry.is_dir() else None
        if match:
            versions.append((int(match.group(1)), int(match.group(2)), entry.name))
    if not versions:
        return "local:unknown"
    return f"local:{max(versions)[2]}"


def sort_key(entry):
    version_match = VERSION_DIR_PATTERN.match(entry["version"])
    minor = int(version_match.group(2)) if version_match else 0
    return (minor, int(entry["number"]))


def cell(value):
    """TSV safety: no tabs, no newlines inside a field."""
    return re.sub(r"[\t\r\n]+", " ", str(value)).strip()


def write_index(entries, out_file, source, notes_dir, provisional=False):
    lines = [
        "# TYPO3 changelog index — GENERATED, do not edit by hand.",
        "# grep-only: never read this file as a whole.",
        f"# source: {source}",
        "# columns: number\ttype\tversion\ttitle\ttags\tsymbols\tmigration-gist\tnote\tsource\tpath",
        "# note column: 'note' means notes/{number}.md exists and takes precedence.",
    ]
    if provisional:
        lines.append(
            "# PROVISIONAL: harvested from an unreleased branch. Entries may still "
            "change or be dropped; never promote to a Validity: line without this caveat."
        )
    for entry in sorted(entries, key=sort_key):
        has_note = (notes_dir / f"{entry['number']}.md").exists()
        lines.append(
            "\t".join(
                cell(value)
                for value in (
                    entry["number"],
                    entry["type"],
                    entry["version"],
                    entry["title"],
                    " ".join(entry["tags"]),
                    " ".join(entry["symbols"]),
                    entry["gist"],
                    "note" if has_note else "-",
                    "provisional" if provisional else source,
                    entry["path"],
                )
            )
        )
    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(entries)


def resolve_output_dir(explicit, guidelines_dir):
    """Maintainer-only write protection.

    Writing generated files into a cloned repository leaves every collaborator
    with a dirty working tree and `git pull` conflicts. Only a checkout marked
    with a `.maintainer` file (gitignored) is written to; everyone else gets a
    local copy outside the repository.
    """
    if explicit:
        return Path(explicit).expanduser(), True

    repo_root = guidelines_dir.parent
    if (repo_root / ".maintainer").exists():
        return guidelines_dir / "typo3" / "changelog-index", True

    fallback = Path.home() / ".claude" / "typo3-changelog"
    return fallback, False


def find_guidelines_dir():
    from_env = os.environ.get("DEVELOPER_GUIDELINES_DIR")
    if from_env:
        return Path(from_env).expanduser()
    # skills/typo3-changelog-harvest/harvest.py -> repository root
    candidate = Path(__file__).resolve().parents[2] / "guidelines"
    if candidate.is_dir():
        return candidate
    return Path.cwd() / "guidelines"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changelog-dir",
        help="path to vendor/typo3/cms-core/Documentation/Changelog (local mode)",
    )
    parser.add_argument(
        "--remote",
        metavar="BRANCH",
        help="harvest from the TYPO3 core repository instead, e.g. --remote main. "
        "Use for versions not installed anywhere yet; implies --provisional.",
    )
    parser.add_argument(
        "--major",
        action="append",
        type=int,
        required=True,
        help="major version to index, repeatable (e.g. --major 13 --major 14)",
    )
    parser.add_argument("--out", help="output directory (overrides maintainer detection)")
    parser.add_argument("--source", help="provenance label, e.g. local:13.4.7")
    parser.add_argument(
        "--provisional",
        action="store_true",
        help="mark entries as coming from an unreleased branch",
    )
    arguments = parser.parse_args()

    if not arguments.changelog_dir and not arguments.remote:
        sys.exit("either --changelog-dir (local) or --remote BRANCH is required")

    changelog_dir = None
    if arguments.changelog_dir:
        changelog_dir = Path(arguments.changelog_dir).expanduser()
        if not changelog_dir.is_dir():
            sys.exit(f"changelog directory not found: {changelog_dir}")

    guidelines_dir = find_guidelines_dir()
    out_dir, is_maintainer = resolve_output_dir(arguments.out, guidelines_dir)
    notes_dir = out_dir / "notes"
    out_dir.mkdir(parents=True, exist_ok=True)
    notes_dir.mkdir(parents=True, exist_ok=True)

    if not is_maintainer:
        print(
            "Read-only mode: no .maintainer marker in the guidelines repository.\n"
            f"Writing to {out_dir} instead, leaving the repository untouched.",
            file=sys.stderr,
        )

    is_provisional = arguments.provisional or bool(arguments.remote)
    if arguments.remote:
        source = arguments.source or f"web:{arguments.remote}"
    else:
        source = arguments.source or detect_source(changelog_dir)

    for major in arguments.major:
        if arguments.remote:
            entries = harvest_remote(major, arguments.remote, out_dir / "cache" / arguments.remote)
        else:
            entries = harvest_local(changelog_dir, major)
        if not entries:
            print(f"v{major}: no entries found, skipped", file=sys.stderr)
            continue
        count = write_index(
            entries,
            out_dir / f"v{major}.tsv",
            source,
            notes_dir,
            provisional=is_provisional,
        )
        by_type = {}
        for entry in entries:
            by_type[entry["type"]] = by_type.get(entry["type"], 0) + 1
        summary = ", ".join(f"{key} {value}" for key, value in sorted(by_type.items()))
        print(f"v{major}.tsv: {count} entries ({summary})")


if __name__ == "__main__":
    main()
