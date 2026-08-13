# Skills

Claude Code skills that work with these guidelines. They live here — not in a
personal `~/.claude/` folder — because they depend on the structure and content
of this repository and must stay in sync with it.

## Installing

Skills are picked up from `~/.claude/skills/` (all projects) or
`<project>/.claude/skills/` (one project). Symlink rather than copy, so a
`git pull` updates the skill too:

```bash
ln -s ~/PhpstormProjects/developer-guidelines/skills/typo3-changelog-harvest \
      ~/.claude/skills/typo3-changelog-harvest
```

## Available skills

| Skill | Purpose |
|---|---|
| [typo3-changelog-harvest](typo3-changelog-harvest/SKILL.md) | Build and query the TYPO3 changelog index (level 3 of the guidelines architecture) |
| [create-content-block](create-content-block/SKILL.md) | Scaffold a TYPO3 Content Block following the shared conventions |
| [guidelines-upgrade](guidelines-upgrade/SKILL.md) | Update a project's guideline references after a restructuring, and check read permissions |
| [changelog-audit](changelog-audit/SKILL.md) | Find changelog entries the guidelines should react to, with a triage log so nothing is judged twice |

## When guidelines move

Add the moves to [guidelines-upgrade/path-map.tsv](guidelines-upgrade/path-map.tsv)
in the same commit. Consuming projects have no other way to find out where a
rule went.

## Write protection

Skills that generate files into this repository check for a `.maintainer` marker
in the repository root. Without it they run read-only and write elsewhere.

The reason is practical: a skill that writes into a cloned repository leaves
every collaborator with a dirty working tree and `git pull` conflicts.
`.maintainer` is gitignored and exists only in the maintainer's checkout —
everyone else reads the committed result.
