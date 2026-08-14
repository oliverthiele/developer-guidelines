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

READ_PERMISSION = "Read(../developer-guidelines/**)"

# Any reference to a markdown file in the guidelines repository, in whatever
# prefix form. Matches the whole path; resolve_reference() decides what it is
# relative to — the repository root or guidelines/.
REFERENCE_PATTERN = re.compile(r"[\w./~-]*(?:developer-guidelines|guidelines)/[\w./-]+\.md")

REPOSITORY_MARKER = "developer-guidelines/"


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


def grant_permission(project_dir):
    """Add the guidelines read permission to .claude/settings.json.

    Kept behind its own flag: rewriting a committed settings file is a different
    kind of change than fixing a stale path, and should be asked for explicitly.
    """
    settings_file = project_dir / ".claude" / "settings.json"
    if settings_file.is_file():
        try:
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return False, "settings.json is not valid JSON — fix it by hand"
    else:
        settings = {}

    permissions = settings.setdefault("permissions", {})
    allowed = permissions.setdefault("allow", [])
    if any("developer-guidelines" in entry for entry in allowed):
        return False, "already present"

    allowed.append(READ_PERMISSION)
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    return True, str(settings_file.relative_to(project_dir))


def global_memory_dir(project_dir):
    """Claude Code keeps per-project memory outside the project.

    ~/.claude/projects/<slug>/memory/, where the slug is the absolute path with
    every non-alphanumeric character turned into a dash. These files name
    guideline paths just like the in-project ones do, and are easy to miss
    because a scan of the project directory never sees them.
    """
    slug = re.sub(r"[^A-Za-z0-9]+", "-", str(project_dir))
    return Path.home() / ".claude" / "projects" / slug / "memory"


def scan_files(project_dir):
    seen = set()
    for pattern in SCAN_GLOBS:
        for path in project_dir.glob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path
    memory_dir = global_memory_dir(project_dir)
    if memory_dir.is_dir():
        for path in sorted(memory_dir.glob("*.md")):
            if path not in seen:
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


def resolve_reference(reference, guidelines_dir):
    """Where a matched reference actually points.

    Not every referenced file lives under guidelines/. AGENTS.md is in the
    repository root and is the prescribed entry point, and skills/ sits next to
    guidelines/ — resolving those against guidelines/ reports the entry point of
    a correctly set up project as missing.

    Returns (path to check, guidelines-relative form or None for repository-root
    files, which the path map never covers).
    """
    if REPOSITORY_MARKER in reference:
        remainder = reference.rsplit(REPOSITORY_MARKER, 1)[1]
        if remainder.startswith("guidelines/"):
            return guidelines_dir.parent / remainder, remainder[len("guidelines/"):]
        return guidelines_dir.parent / remainder, None
    remainder = reference.rsplit("guidelines/", 1)[1]
    return guidelines_dir / remainder, remainder


def find_dangling(text, guidelines_dir, moves):
    """Referenced guideline files that do not exist and the map cannot fix."""
    known_old = {old for _, old, _ in moves}
    dangling = []
    for match in REFERENCE_PATTERN.finditer(text):
        reference = match.group(0)
        target, relative = resolve_reference(reference, guidelines_dir)
        label = relative if relative is not None else reference
        if label in known_old or label in dangling:
            continue
        if not target.exists():
            dangling.append(label)
    return dangling


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="project root (default: current directory)")
    parser.add_argument("--apply", action="store_true", help="write changes instead of reporting")
    parser.add_argument(
        "--grant-read",
        action="store_true",
        help="add the guidelines read permission to .claude/settings.json (needs --apply)",
    )
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
        if arguments.apply and arguments.grant_read:
            written, detail = grant_permission(project_dir)
            if written:
                print(f"  read permission: added to {detail}")
            else:
                print(f"  read permission: not added — {detail}")
        else:
            print(
                f'  read permission: MISSING — add "{READ_PERMISSION}" to '
                ".claude/settings.json, or re-run with --apply --grant-read"
            )

    changed_files = 0
    total_moves = 0
    dangling_total = []
    for path in sorted(scan_files(project_dir)):
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text, applied = rewrite(text, moves)
        dangling = find_dangling(new_text, guidelines_dir, moves)
        try:
            relative = path.relative_to(project_dir)
        except ValueError:
            relative = path  # global memory, outside the project
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
