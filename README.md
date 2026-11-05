# OSS Maintainer Workflows

Small, reviewable AI-assisted drafts for recurring open-source maintenance work. The toolkit accepts context you provide, validates and previews it locally, redacts common identifiers by default, and can optionally ask the OpenAI Responses API for a schema-constrained draft. It never connects to GitHub or changes a repository.

## Five workflows

- **Issue triage** suggests a category, priority, missing details, and a reply draft without promising timelines or assigning people.
- **Pull request review support** identifies concrete risks supported by the supplied diff and asks for evidence; it cannot approve or merge a pull request.
- **CI failure diagnosis** points to the first actionable failure and a focused verification step, without recommending that security checks be disabled.
- **Release note drafting** organizes supplied merged pull requests and avoids unsupported security, compatibility, or breaking-change claims.
- **Security advisory triage** compares an advisory with supplied package inventory and reports confirmed, ruled-out, or unknown exposure for a maintainer to verify.

All five are drafts. A maintainer must verify facts, tone, security conclusions, and project policy before acting. Repository text, logs, diffs, and advisory descriptions are treated as untrusted input.

## Install and run

Requires Python 3.11 or newer. Core validation and preview use only the Python standard library.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
maintainerkit issue-triage examples/issue.json
```

The default command validates, redacts common credentials, emails, and IPv4 addresses, and prints the exact sanitized context locally. It makes no network request.

To request a draft, install the optional SDK and explicitly opt in after inspecting the preview:

```bash
pip install -e '.[api]'
export OPENAI_API_KEY='your API key'
export OPENAI_MODEL='a model available to your API account'
maintainerkit issue-triage examples/issue.json --send-to-openai
```

The selected model is configured at runtime because availability depends on the API account. To include identifiers, add `--include-identifiers`; inspect the displayed context carefully first. The program does not load `.env` files or read credentials from repository data.

Other examples: `pr-review examples/pull-request.json`, `ci-diagnosis examples/ci-failure.json`, `release-draft examples/release.json`, and `advisory-triage examples/advisory.json`.

## Data handling

No GitHub credentials, repository access, telemetry, or automatic uploads are implemented. An API request sends the shown JSON context and workflow instructions to the OpenAI API. The adapter sets `store=False`, which disables Responses application-state storage for that request; it does not disable API abuse-monitoring logs. OpenAI states that abuse-monitoring logs may retain customer content for up to 30 days by default, subject to its policies and eligible data controls. API data is not used to train models unless the customer opts in. Review current [API data controls](https://developers.openai.com/api/docs/guides/your-data) and your organization's settings before sending sensitive material. Redaction is best-effort and is not a substitute for data minimization or review.

## Design and limitations

- Strict JSON schema output is validated again locally.
- Input is bounded to 120,000 characters per text field and 300 KB serialized total; lists are capped at 250 entries.
- Common token formats, email addresses, IPv4 strings, and secret-like object keys are redacted by default. This is not a comprehensive secret scanner.
- Prompt injection defenses reduce risk but cannot make model output trustworthy. Never treat a draft as approval, a security finding as confirmed, or a release note as fact without review.
- The tool does not fetch current data, check package registries, execute code, inspect a live repository, or take actions in GitHub.
- Costs depend on the API model and input/output size. Preview first and keep submitted context minimal.

## Roadmap

1. Establish baseline fixtures and document supported context shapes.
2. Add maintainer-contributed examples and validate schemas against real, sanitized cases.
3. Add evaluation fixtures for unsupported claims, prompt injection, and sensitive-data handling.
4. Consider optional GitHub read-only adapters only after the core stays useful offline; any write capability would require a separate explicit design and approval step.
5. Publish versioned releases with changelog, compatibility notes, and reviewed security advisories.

Contributions, failure cases, and workflow requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the issue templates. This is a new project; adoption and ecosystem impact must be demonstrated over time, not assumed.

## License

MIT. See [LICENSE](LICENSE).
