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

## Scripts that run on the host and inside the DDEV container

**Basis:** documented — `IS_DDEV_PROJECT` is set in the container only,
[DDEV: Custom commands](https://docs.ddev.com/en/stable/users/extend/custom-commands/)

**Basis: observed** — a `ddev` command run inside the web container does not
fail. It prints `not available inside container` and exits 0, so `set -e` does
not notice. A script that called `ddev mysql` there reported success for every
step and had written nothing.

Looking for the `ddev` binary and `.ddev/config.yaml` does not tell host and
container apart — the container sees both. Check `IS_DDEV_PROJECT` first:

```bash
if [[ "${IS_DDEV_PROJECT:-}" == "true" ]]; then
    typo3=(vendor/bin/typo3)                  # inside the web container
elif command -v ddev >/dev/null 2>&1 && [[ -f .ddev/config.yaml ]]; then
    typo3=(ddev exec typo3)                   # on the host
else
    typo3=(vendor/bin/typo3)                  # on a server
fi
"${typo3[@]}" cache:flush
```

When an `--execute` run reports success and nothing changed, suspect this first.

## Long-running Composer scripts under DDEV

**Basis:** observed — the opt-out itself is documented in
[Composer: Managing process timeouts](https://getcomposer.org/doc/articles/scripts.md#managing-process-timeouts)

DDEV sets `COMPOSER_PROCESS_TIMEOUT` in the web container (2000 seconds where
it was observed — `ddev exec printenv COMPOSER_PROCESS_TIMEOUT` shows the value).
Composer stops a script after that time with `exceeded the timeout of … seconds`,
halfway through. A script that can run longer — a crawl, a full index, a link
check — starts with the opt-out:

```json
"scripts": {
    "check:links": [
        "Composer\\Config::disableProcessTimeout",
        "@php vendor/bin/typo3 my:long-command"
    ]
}
```

## Remote commands run in the remote login shell — never assume bash

**Basis:** observed

A command passed to `ssh host "…"` is interpreted by the target user's login
shell, not by the shell the script runs in. On servers set up with zsh as login
shell, zsh behaves differently from bash in exactly the places scripts rely on:

- an unmatched glob aborts the command (`no matches found`) instead of being
  passed on literally — an argument like `'*.add,*.change'` for a CLI tool breaks
- an unquoted `$VARIABLE` is not split on whitespace
- `$name:x` is read as a history modifier, not as `$name` followed by `:x`

A script that orchestrates servers over ssh therefore does one of these:

- pass SQL and scripts on stdin instead of on the command line:
  `printf '%s\n' "$sql" | ssh host "mysql database"`
- quote every argument for the remote side: `printf '%q ' "$@"`
- run the remote part explicitly in bash: `ssh host bash -s <<'EOF' … EOF`

Deployer is not affected: `run()` executes through its `shell` setting, which is
`bash -ls` by default, whatever the login shell of the deploy user is — checked
in deployer/deployer 7.5.12.

### A non-interactive command lacks what `~/.bashrc` sets up

**Basis:** observed

Tools put on the `PATH` in `~/.bashrc` — nvm is the usual one — are missing in
`ssh host 'command'`, and `bash -lc` does not bring them back. The usual cause
is a guard at the top of `~/.bashrc` that returns for non-interactive shells and
so skips every line below it. Load the tool in the command itself:

```bash
ssh deploy@example.com 'export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; \
    cd /var/www/project/Build && npm run build'
```

### Long-running jobs are started detached

**Basis:** observed

A job started in a plain ssh session dies when the connection drops — at its
next write to the closed terminal. Anything that runs longer than a few
minutes — a full index, a reference index rebuild — is started detached, with
its output in a log file:

```bash
ssh deploy@example.com 'cd /var/www/project && setsid nohup vendor/bin/typo3 my:long-command \
    > var/log/long-command-$(date +%Y%m%d-%H%M%S).log 2>&1 < /dev/null &'
```
