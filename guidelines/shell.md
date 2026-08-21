---
title: Shell scripting
scope: shell
applies_to:
  - "**/*.sh"
  - "**/*.bash"
see_also: ["git.md"]
---
# Shell / Bash Guidelines

Conventions for shell scripts that run across macOS hosts, DDEV containers,
and Live/Staging servers.

These rules are mandatory unless explicitly overridden.

---

## Why this file exists

macOS ships bash 3.2 by default (Apple does not update it, due to bash 4+
switching to the GPLv3 license) while DDEV and Live/Staging servers run
bash 5.x. A script that behaves correctly under one can fail under the other.

A concrete failure: a cleanup script (an `rm -rf` loop over several paths) ran
directly on a macOS host under `set -euo pipefail`. Mid-run it hit a path
whose array had already emptied out, `"${array[@]}"` raised an "unbound
variable" error, and `set -e` aborted the script immediately — leaving the
remaining deletions undone. No data was lost, but the abort happened mid-way
through a destructive operation, which is the dangerous case to design against.

The root cause: under `set -u`, `"${array[@]}"` throws "unbound variable" on
an empty array in bash 3.2, but not in bash 4.4+, where this was fixed. A
dry run and an `--execute` run do not necessarily hit the empty-array case the
same way, so this is easy to miss in manual testing.

## Rules

- **Guard every `"${array[@]}"` expansion under `set -u`** with an emptiness
  check before iterating, regardless of which bash version the script is
  expected to run under:

  ```bash
  if (( ${#array[@]} > 0 )); then
    for item in "${array[@]}"; do
      ...
    done
  fi
  ```

  This is cheap insurance and protects against exactly the bash-3.2-vs-4.4+
  gap above, independent of which host ends up running the script.

- **Run non-DDEV-orchestrating shell scripts through `ddev exec bash <script>`
  instead of directly on the macOS host.** A script that does not itself call
  `ddev` commands (`ddev import-db` and similar host-only orchestration is the
  exception) should execute under the same bash version as DDEV and
  Live/Staging, which sidesteps the 3.2-vs-5.x gap entirely rather than
  requiring every script to be written defensively enough to work on both.
