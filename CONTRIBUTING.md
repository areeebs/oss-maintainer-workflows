# Contributing

Issues and pull requests are welcome. For a change, explain the maintainer problem it addresses, include a small sanitized example where useful, and document any new network or data handling. Keep API use opt-in, preserve offline preview, and never add automatic GitHub writes. Do not include real credentials, private repository data, or personal data in fixtures. Please describe how you manually checked your change; this project does not yet promise a stable API.

## Review expectations

Keep workflow behavior narrow and project-neutral. Findings should be tied to supplied evidence, uncertainty should remain visible, and people must retain control of project decisions. Changes to prompts, schemas, redaction, API transmission, or generated content need a clear explanation and updated documentation. Avoid adding a dependency unless it materially improves the maintainer experience.

## Release practice

Until a release process is established, changes land through reviewed pull requests and are documented in `CHANGELOG.md`. Once a release is cut, the maintainer should tag the reviewed commit, publish notes from merged work, and include compatibility or privacy changes explicitly.
