#!/usr/bin/env python3
"""Maintain main branch locally and remotely without mocks.

- Merge origin/master into main if exists
- Push main
- Delete remote master
- Set default branch to main (via gh if available, else manual UI)
- Prune stale refs
- Remove local master if present
"""

from __future__ import annotations

import os
import subprocess
import sys
from shutil import which


def run(cmd, check=True, capture=False, shell=False):
    print("$ ", cmd if isinstance(cmd, str) else " ".join(cmd))
    result = subprocess.run(
        cmd, shell=shell, check=check, text=True, capture_output=capture
    )
    return result.stdout if capture else None


def has_remote_branch(branch: str) -> bool:
    try:
        out = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", branch],
            capture_output=True,
            text=True,
        )
        return bool(out.stdout.strip())
    except Exception:
        return False


def main():
    BRANCH_MAIN = "main"
    BRANCH_MASTER = "master"
    repo = "https://github.com/rsdenck/ollamaagent.git"

    # 1) Fetch and ensure main is current
    run(["git", "fetch", "origin"])
    run(["git", "checkout", BRANCH_MAIN])
    run(["git", "pull", "origin", BRANCH_MAIN])

    # 2) Merge origin/master if exists
    if has_remote_branch(BRANCH_MASTER):
        print("Mesclando origin/master em main...")
        try:
            run(
                [
                    "git",
                    "merge",
                    f"origin/{BRANCH_MASTER}",
                    "--no-ff",
                    "-m",
                    "Merge origin/master into main: consolidar alterações",
                ]
            )
        except subprocess.CalledProcessError:
            print(
                "Conflitos detectados durante a mesclagem. Resolva os conflitos, adicione e faça o commit, depois continue manualmente."
            )
            sys.exit(1)
    else:
        print("origin/master não existe no remoto; pulando merge.")

    # 3) Push main
    run(["git", "push", "origin", BRANCH_MAIN])

    # 4) Delete remote master
    if has_remote_branch(BRANCH_MASTER):
        run(["git", "push", "origin", "--delete", BRANCH_MASTER])
    else:
        print("Remote master já não existe.")

    # 5) Set default branch to main
    if which("gh"):
        token = os.environ.get("GH_TOKEN")
        if token:
            # Authenticate with token
            gh = which("gh")
            # gh auth login --with-token requires a heredoc; emulate via shell input
            import subprocess

            subprocess.run(
                [gh, "auth", "login", "--with-token"],
                input=token,
                text=True,
                check=False,
            )
        # Attempt to set default branch; ignore failures
        subprocess.run(
            [
                "gh",
                "repo",
                "edit",
                "rsdenck/ollamaagent",
                "--default-branch",
                BRANCH_MAIN,
            ],
            check=False,
        )
    else:
        print(
            "gh não detectado; altere o default pela UI do GitHub. Settings > Branches > Default branch -> main"
        )

    # 6) Cleanup local refs
    run(["git", "fetch", "--prune"])
    run(["git", "remote", "prune", "origin"])
    print("Branches remotas após prune:")
    run(["git", "branch", "-r"])

    # 7) Remove local master
    run(["git", "branch", "-D", BRANCH_MASTER])

    print(
        "Concluído. Verifique no GitHub se apenas main continua como branch e se é o default."
    )


if __name__ == "__main__":
    main()
