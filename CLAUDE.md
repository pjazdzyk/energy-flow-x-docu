# CLAUDE.md

The public documentation repository (github.com/pjazdzyk/energy-flow-x-docu): Markdown, images and the
Python scripts under `validation-evidence/` that regenerate the reference figures. No build, no
dependency on the other workspace projects.

- Everything here is public and makes claims about the products. A capability that ships is not
  finished until `README.md` (the product showcase: capabilities, fluids, access tiers, references)
  says so, and a claim must match what the code does today.
- Legal and IP rules apply to all text: follow the `legal-ip-policy` skill (which sources may be
  named, how standards are cited, clean-room wording) before adding or editing references or citations.
- `validation-evidence/` holds re-runnable comparisons (scene files, reference scripts, expected figures).
  Change a figure only by re-running its script, never by editing the number by hand.
- The repo was named `energy-flow-x-demo` until 2026-07; use the current name in links (the UI's
  `publicRepoLinks.test.js` fails the build on the old one).
- Keep secrets, private paths and unreleased plans out: this repository is world-readable.
