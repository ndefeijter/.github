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

## Rules

- A repository adds no issue templates of its own: one local template switches off all shared ones there.
- GitHub only fills in a template in the browser. From the command line, read the file here and follow its structure:

  ```bash
  gh api repos/ndefeijter/.github/contents/.github/ISSUE_TEMPLATE/task.md -H "Accept: application/vnd.github.raw"
  ```
- This repository is public. Nothing goes in that isn't meant to be read by everyone.
