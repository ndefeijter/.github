#!/usr/bin/env python3
"""Check a pull request against the rules for title, description and branch.

Reads the pull request from environment variables, because all of it is input
from outside and must never be pasted into a shell command:

  PR_BODY           the description
  PR_BRANCH         the name of the branch that is merged
  PR_AUTHOR_IS_BOT  "true" when a bot opened the pull request

Prints one error per broken rule and exits with 1 when there is any.
"""

import os
import re
import sys

KINDS = ("feat", "fix", "docs", "chore")
BRANCH = re.compile(r"^(%s)/[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$" % "|".join(KINDS))
CLOSES = re.compile(r"\bCloses #[0-9]+\b")
ATTRIBUTION = re.compile(
    r"^[^A-Za-z\n]*(Co-Authored-By:|Generated (with|by) )", re.IGNORECASE | re.MULTILINE
)


def check(body, branch, author_is_bot):
    """Return a list of (rule, how to fix it) for every broken rule."""
    errors = []
    if ATTRIBUTION.search(body):
        errors.append((
            "No agent attribution",
            "The description has a `Co-Authored-By:` or `Generated with …` line. Remove it: "
            "the commits already show who made them.",
        ))
    # A bot doesn't use the templates, and its descriptions may contain HTML comments.
    if not author_is_bot:
        if "<!--" in body:
            errors.append((
                "No template leftovers",
                "The description contains `<!--`. Remove the hints from the template: "
                "the description becomes the commit message on main.",
            ))
        if not CLOSES.search(body):
            errors.append((
                "Traceable",
                "The description has no `Closes #<issue number>`. Add it as the last line; "
                "create the issue first when there is none.",
            ))
        if not BRANCH.match(branch):
            errors.append((
                "Branch name",
                "The branch is not named `<kind>/<issue number>-<short-title>`, with %s as the "
                "kind and lowercase words joined by hyphens, like `feat/1-contact-form`. "
                "A branch can't be renamed in a pull request: open a new one from a branch "
                "with the right name." % ", ".join("`%s`" % kind for kind in KINDS),
            ))
    return errors


def main():
    errors = check(
        os.environ.get("PR_BODY", ""),
        os.environ.get("PR_BRANCH", ""),
        os.environ.get("PR_AUTHOR_IS_BOT", "") == "true",
    )
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    lines = ["## Pull request rules", ""]
    if not errors:
        lines.append("The pull request follows the rules.")
    for rule, fix in errors:
        # The messages are fixed text; nothing from the pull request is echoed.
        print("::error title=%s::%s" % (rule, fix))
        lines.append("- **%s.** %s" % (rule, fix))
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("\n".join(lines) + "\n")
    else:
        print("\n".join(lines))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
