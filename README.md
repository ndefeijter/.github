# Shared GitHub files

The issue and pull request templates for all repositories of this account. GitHub uses them in every repository that has none of its own.

## Issue types

| Template | When | Label |
| --- | --- | --- |
| **Feature** | Adds value to what the repository delivers | `feature` |
| **Task** | Makes delivery possible, or better, more reliable or cheaper. Nothing changes for the user of the result. | `task` |
| **Bug** | An existing feature of the product doesn't work as intended | `bug` |

The labels must exist in each repository; a template can't create them.

## Pull requests

Repositories squash-merge with the pull request title and description as the commit. The pull request template is therefore short and written as a commit message.

The hints in the template are HTML comments. GitHub copies them into the commit message, so remove them from the description; the check below refuses a description that still has one.

## Pull request check

A check that every repository can run on its pull requests. It fails when:

| Rule | The pull request |
| --- | --- |
| No template leftovers | has `<!--` in its description |
| Traceable | has no `Closes #<issue number>` in its description |
| Branch name | comes from a branch that is not named `<kind>/<issue number>-<short-title>`, with `feat`, `fix`, `docs` or `chore` as the kind |
| No agent attribution | has a `Co-Authored-By:` or `Generated with …` line in its description |

A pull request opened by a bot, such as a dependency update, skips "Traceable" and "Branch name".

To run it in a repository, add `.github/workflows/pull-request.yml`:

```yaml
name: Pull request

on:
  pull_request:
    types: [opened, edited, reopened, synchronize]

permissions:
  contents: read

jobs:
  rules:
    name: rules
    uses: ndefeijter/.github/.github/workflows/pull-request-rules.yml@main
```

`edited` makes the check run again when only the description changes, so fixing the description is enough. The check blocks a merge only when a ruleset on `main` requires the status check `rules / check`; without one it shows as failed and the merge button keeps working.

The rules are in [`scripts/pull_request_rules.py`](scripts/pull_request_rules.py). Callers use `@main`, so a change to the script applies everywhere at once.

## Rules

- A repository adds no issue templates of its own: one local template switches off all shared ones there.
- GitHub only fills in a template in the browser. From the command line, read the file here and follow its structure:

  ```bash
  gh api repos/ndefeijter/.github/contents/.github/ISSUE_TEMPLATE/task.md -H "Accept: application/vnd.github.raw"
  ```
- This repository is public. Nothing goes in that isn't meant to be read by everyone.
