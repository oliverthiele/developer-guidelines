#!/usr/bin/env python3
"""Bring a project's references to the shared developer guidelines up to date.

Checks three things in the current project:

1. the shared guidelines can be found at all
2. reading them is pre-granted in .claude/settings.json
3. every guideline path referenced in the project still exists — stale paths are
   rewritten using path-map.tsv

Reports by default; only --apply writes. Nothing is ever committed.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Files that typically name guideline paths. Globs, relative to the project root.
SCAN_GLOBS = [
    "CLAUDE.md",
    "AGENTS.md",
    ".claude/memory/*.md",
    ".claude/*.md",
    "Guidelines/*.md",
    "Guidelines/**/*.md",
    "docs/*.md",
]

READ_PERMISSION = "Read(../developer-guidelines/guidelines/**)"

# Any reference to a markdown file below guidelines/, in whatever prefix form.
REFERENCE_PATTERN = re.compile(r"(?:[\w./~-]*guidelines/)?([\w./-]+\.md)")


def load_path_map(skill_dir):
    moves = []
    for line in (skill_dir / "path-map.tsv").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        release, old, new = (part.strip() for part in parts)
        moves.append((release, old, new))
    # Longest first, so typo3/v13/integrator.md is handled before any shorter
    # pattern that could also match part of it.
    moves.sort(key=lambda move: len(move[1]), reverse=True)
    return moves


def find_guidelines_dir(project_dir):
    candidates = [
        project_dir.parent / "developer-guidelines" / "guidelines",
        Path.home() / "PhpstormProjects" / "developer-guidelines" / "guidelines",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def guidelines_release(guidelines_dir):
    """Latest released version, read from the repository's CHANGELOG."""
    changelog = guidelines_dir.parent / "CHANGELOG.md"
    if not changelog.is_file():
        return None
    for line in changelog.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^## \[(\d+\.\d+\.\d+)\]", line)
        if match:
            return match.group(1)
    return None


def check_permission(project_dir):
    """Is reading the shared guidelines pre-granted?

    Without it every read prompts, which is what makes people copy guideline
    text into the project instead of referencing it.
    """
    for name in (".claude/settings.json", ".claude/settings.local.json"):
        settings_file = project_dir / name
        if not settings_file.is_file():
            continue
        try:
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None, f"{name} is not valid JSON"
        allowed = settings.get("permissions", {}).get("allow", [])
        if any("developer-guidelines" in entry for entry in allowed):
            return True, name
    return False, None


def scan_files(project_dir):
    seen = set()
    for pattern in SCAN_GLOBS:
        for path in project_dir.glob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def stem_variants(old, new):
    """Legacy names also appear without the .md suffix, in prose and lists.

    Only hyphenated legacy names qualify: "typo3-developer" is unambiguous,
    whereas a bare "xliff" or "integrator" would match far too much.
    """
    old_stem, new_stem = old[:-3], new[:-3]
    if "-" in Path(old_stem).name and old_stem.endswith(Path(old_stem).name):
        return [(old_stem, new_stem)]
    return []


def rewrite(text, moves):
    """Apply the path map. Returns (new text, list of applied moves)."""
    applied = []
    for release, old, new in moves:
        if old in text:
            text = text.replace(old, new)
            applied.append((release, old, new))
        for old_variant, new_variant in stem_variants(old, new):
            if old_variant in text:
                text = text.replace(old_variant, new_variant)
                applied.append((release, old_variant, new_variant))
    return text, applied


def find_dangling(text, guidelines_dir, moves):
    """Referenced guideline files that do not exist and the map cannot fix."""
    known_old = {old for _, old, _ in moves}
    dangling = []
    for match in REFERENCE_PATTERN.finditer(text):
        if "guidelines/" not in match.group(0):
            continue
        reference = match.group(1)
        if reference in known_old or reference in dangling:
            continue
        if not (guidelines_dir / reference).exists():
            dangling.append(reference)
    return dangling


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="project root (default: current directory)")
    parser.add_argument("--apply", action="store_true", help="write changes instead of reporting")
    arguments = parser.parse_args()

    project_dir = Path(arguments.project).expanduser().resolve()
    skill_dir = Path(__file__).resolve().parent
    moves = load_path_map(skill_dir)

    print(f"Project: {project_dir}")

    guidelines_dir = find_guidelines_dir(project_dir)
    if guidelines_dir is None:
        print(
            "  guidelines: NOT FOUND — clone developer-guidelines next to this "
            "project, or set DEVELOPER_GUIDELINES_DIR"
        )
        return 1
    release = guidelines_release(guidelines_dir)
    print(f"  guidelines: {guidelines_dir}" + (f" (release {release})" if release else ""))

    granted, source = check_permission(project_dir)
    if granted:
        print(f"  read permission: granted in {source}")
    elif granted is None:
        print(f"  read permission: {source}")
    else:
        print(f'  read permission: MISSING — add "{READ_PERMISSION}" to .claude/settings.json')

    changed_files = 0
    total_moves = 0
    dangling_total = []
    for path in sorted(scan_files(project_dir)):
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text, applied = rewrite(text, moves)
        dangling = find_dangling(new_text, guidelines_dir, moves)
        relative = path.relative_to(project_dir)
        if applied:
            changed_files += 1
            total_moves += len(applied)
            print(f"  {relative}")
            for _, old, new in applied:
                print(f"      {old}  ->  {new}")
            if arguments.apply:
                path.write_text(new_text, encoding="utf-8")
        if dangling:
            dangling_total.append((relative, dangling))

    if dangling_total:
        print("\n  Referenced but missing, and not covered by the path map:")
        for relative, references in dangling_total:
            for reference in references:
                print(f"      {relative}: {reference}")
        print("  These need a human decision — check whether the rule moved or was dropped.")

    if not changed_files:
        print("  references: up to date")
    elif arguments.apply:
        print(f"\n  applied {total_moves} moves in {changed_files} file(s) — review and commit")
    else:
        print(f"\n  {total_moves} move(s) in {changed_files} file(s) — re-run with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
