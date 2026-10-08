# Setup

How to place this repository next to a project, and how a project's own
`Guidelines/` folder relates to it. Read once per project — it is not part of
the per-task read path. Which file holds which rules is listed in the
[routing table in `AGENTS.md`](../AGENTS.md#routing).

Clone this repository as a sibling directory next to your projects:

```
PhpstormProjects/
├── developer-guidelines/    ← this repo
├── my-project-a/
├── my-project-b/
└── ...
```

The default path used in `CLAUDE.md` and memory files is
`../developer-guidelines/guidelines/` (relative to the project root).

**Only the sibling relationship is binding, not the parent directory name.** The
tree above happens to be called `PhpstormProjects/`, but nothing depends on that —
every reference is relative. Teams that share a location should name it in their
own project guidelines, so onboarding commands can be copied verbatim.

If the guidelines are located elsewhere, set the environment variable
`DEVELOPER_GUIDELINES_DIR` to the absolute path of the `guidelines/` directory.

Update with `git pull` in this repository — every project reads it directly, so there
is no copy to refresh.

Projects read the **working tree**, not a tag. Whatever branch this clone has
checked out is what every project sees, so keep it on `main` and switch
deliberately when working on the guidelines themselves — otherwise a project
silently reads unreleased rules. Do not vendor these files into a project (no submodule, no
duplication); that would pin each project to a commit and defeat the single pull.

## Project-specific guidelines

Rules that hold for one project only — CSS prefix assignments, build paths, extension
conventions — do not belong in this repository. They live in a `Guidelines/` folder in
the project root, committed with the project:

```
PhpstormProjects/
├── developer-guidelines/    ← this repo, shared rules
└── my-project/
    └── Guidelines/
        └── README.md        ← index of the project rules
```

**`Guidelines/` is evaluated first**, before any file in this repository — comparable to
`Configuration/TCA/Overrides/` in TYPO3, which refines the base definition rather than
replacing it. One difference matters: nothing loads `Guidelines/` automatically. The
project's own `CLAUDE.md` has to point at it, which is what the setup below does.

**On conflict, the project file wins.** Every override there names the shared rule it
replaces and the reason for it.

Never copy shared rules into a project folder. If a rule holds for every project,
propose it here instead.

The folder is spelled `Guidelines/` with a capital G in every project. This is binding:
macOS resolves paths case-insensitively, Linux and CI do not, so a mixed spelling works
on one machine and silently fails on another.

## Setting up a project

Three steps, once per project.

**1.** Create `Guidelines/README.md` as the index — precedence rule, and a table naming
which file covers which work area.

**2.** Point the project's `CLAUDE.md` at both — the project rules and the shared entry
point. The project file must be self-contained — never refer to a personal
`~/.claude/CLAUDE.md`, since collaborators do not have it:

```markdown
## Guidelines — mandatory read protocol

Project rules live in `Guidelines/` and are read first; on conflict, the project file
wins. The shared, project-independent guidelines are cloned next to this project in
`../developer-guidelines/`. Their entry point,
`../developer-guidelines/AGENTS.md`, is imported below — read order, routing table,
what to do when a rule is missing. Its paths are relative to `../developer-guidelines/`.

@Guidelines/README.md

@../developer-guidelines/AGENTS.md

Never edit files in `../developer-guidelines/` without explicit confirmation.
```

A project without a `Guidelines/` folder uses the same block without the first
sentence and the `@Guidelines/README.md` line.

**Import, do not copy.** The block holds no shared rule of its own. Read order,
routing and *When a rule is missing* come in through the import, so a change in this
repository reaches every project with the next `git pull` — a copied summary would
stay behind, as the one this template used to carry did.

- **The first session asks once** whether to allow the import, because it points
  outside the project. Allow it. Declined, it stays off without asking again, and
  the guidelines are only reached through the sentence above it.
- **The sentence naming `../developer-guidelines/AGENTS.md` stays** for that case,
  and for assistants that do not follow `@` imports.
- **A project `AGENTS.md`**, if the project has one, gets the same block. Tools that
  read `AGENTS.md` but not `@` imports find the shared entry point through the
  sentence.
- **Twice is harmless.** A personal `~/.claude/CLAUDE.md` that imports the same
  file loads it a second time in that project — a few kilobytes, and both copies
  are the same text.

**3.** Commit `.claude/settings.json` so reading the shared guidelines does not prompt
every collaborator:

```json
{
  "permissions": {
    "allow": [
      "Read(../developer-guidelines/**)"
    ]
  }
}
```

The grant covers the whole repository, not just `guidelines/` — `AGENTS.md` in the
root is the entry point, and `skills/` is read from projects that run
`guidelines-upgrade`. Both sit outside a `guidelines/**` pattern, so a narrower
grant prompts on exactly the files a project reads first. Nothing here is writable
by a project, so there is no risk in the wider read.
