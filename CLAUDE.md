# Working in this repository

## Git: pull, merge and push automatically

The owner has given standing permission for Claude to finish every change end to end without asking:

1. Before starting, pull the latest `main` and start the working branch from it.
2. Commit the change on the working branch and push it.
3. Open a pull request into `main` (not a draft) and merge it yourself.
4. Pull `main` again so the next change starts from the merged code.

Always go through a pull request; never push straight to `main`. Stop and ask the owner instead of merging when there is a merge conflict that needs a decision, a check fails for a reason this change caused, or a change deletes pages or content.

The Cloudflare "Workers Builds" check currently fails on every non-`main` branch, before any upload, for a reason that only shows in the Cloudflare dashboard log. That known failure does not block a merge.

## The site

- The `.html` pages are generated: edit `tools/build.py` (and prices in `tools/menu.py`), then run `python3 tools/build.py` and commit the regenerated pages. Never hand-edit a generated `.html` file.
- `styles.css`, `site.js`, `book.js` and `tour.js` are edited directly.
- Anything that is not part of the website must be listed in `.assetsignore`, because the repository root is published as-is.
