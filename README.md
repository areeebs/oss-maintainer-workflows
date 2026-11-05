# OSS Maintainer Workflows

**Evidence-grounded, human-reviewed AI drafts for recurring open-source maintenance.** Triage an issue, inspect a proposed change, understand a failed CI run, prepare release notes, or assess a dependency advisory. Context is validated and previewed locally; an API request happens only after you opt in.

This project is for maintainers who want help with the first pass while keeping decisions, repository access, and final communication in human hands.

## What it does

**Issue triage** organizes a report into a likely category, priority, missing details, and a concise response draft. It will not confirm a bug, promise a response time, or assign a person without evidence.

**Pull request review support** looks for concrete correctness, security, compatibility, and coverage concerns in the diff you provide. Each finding must quote an exact excerpt from your supplied context. It does not approve, merge, or rewrite the change.

**CI failure diagnosis** identifies the earliest actionable failure, separates it from likely downstream noise, and suggests the smallest next check. It will not advise disabling security controls or exposing secrets.

**Release-note drafting** groups user-facing changes from supplied merged pull requests and preserves their references. Security, breaking-change, and compatibility claims require supporting input.

**Security advisory triage** compares an advisory with a package inventory you provide. It reports confirmed, ruled-out, or unknown exposure based only on that evidence; it does not claim to scan your repository or install a fix.

## Why this project

Maintainers repeat the same cognitively expensive first-pass work across issues, patches, build logs, releases, and advisories. General chat prompts leave maintainers to assemble context, preserve project policy, and check whether a claim is supported. This toolkit makes those steps explicit in five bounded workflows with a shared input contract, schema-constrained results, evidence excerpts, local preview, and a clear human-review step.

The goal is useful work for small and understaffed projects as well as larger projects. It is not an autonomous maintainer or an alternative to project-specific review.

## Quick start

Requires Python 3.11 or later. The preview path has no third-party runtime dependencies and makes no network request.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
maintainerkit issue-triage examples/issue.json
```

Preview validates the input, redacts common credentials and identifiers, then prints the exact context that would be used and its SHA-256 fingerprint. Nothing is sent. API use requires a second command with the matching fingerprint, so edits to the input or privacy options invalidate the review confirmation.

To generate a draft with the OpenAI API:

```bash
pip install -e '.[api]'
export OPENAI_API_KEY='your API key'
export OPENAI_MODEL='a model available to your API account'
maintainerkit issue-triage examples/issue.json
# Review the printed JSON and fingerprint, then paste that fingerprint below.
maintainerkit issue-triage examples/issue.json --send-to-openai --confirm-context-sha256 YOUR_REVIEWED_SHA256
```

The API model is set at runtime because availability depends on your account. Results are formatted as Markdown for review. To save a draft locally, add `--output triage-draft.md`; to save structured output, add `--result-format json`. To include identifiers, add `--include-identifiers` to both the preview and send commands, inspect the full context, and confirm the new fingerprint. Keep submitted context minimal.

### Use the other workflows

```bash
maintainerkit pr-review examples/pull-request.json
maintainerkit ci-diagnosis examples/ci-failure.json
maintainerkit release-draft examples/release.json
maintainerkit advisory-triage examples/advisory.json
```

The commands above only preview. To request a draft, repeat the workflow command with `--send-to-openai --confirm-context-sha256` and the fingerprint from the reviewed preview. All example data is synthetic.

## Trust and safety boundaries

- No GitHub token, repository connection, telemetry, automatic upload, label, comment, approval, merge, release, or code edit is implemented.
- API access is opt-in and requires the SHA-256 fingerprint of a reviewed preview. Any change to the context or redaction option requires a fresh preview and fingerprint.
- Prompt instructions treat issue text, diffs, logs, and advisory text as untrusted data.
- Structured output is checked locally. Every finding's evidence must be an exact substring of the context provided to the workflow. This prevents unsupported quotations, but it does not prove the model interpreted a quote correctly.
- A maintainer must verify findings, priority, release language, and advice against project policy before use. Model output can still be wrong or incomplete.
- The security-advisory workflow is a triage aid, not vulnerability detection or remediation.

## Data handling

An API request sends the displayed JSON context and workflow instructions to the OpenAI API. The adapter sets `store=False`, which disables Responses application-state storage for that request; it does not disable API abuse-monitoring logs. OpenAI states that abuse-monitoring logs may retain customer content for up to 30 days by default, subject to policies and eligible data controls. API data is not used to train models unless the customer opts in. Review current [API data controls](https://developers.openai.com/api/docs/guides/your-data) and your organization's settings before sending sensitive material. Redaction is best-effort, not a secret scanner.

## Design references

The project borrows design lessons from established open-source tools without copying their functionality. [reviewdog](https://github.com/reviewdog/reviewdog) demonstrates focused diagnostics that can be filtered to a patch and reviewed locally. [OpenSSF Scorecard](https://github.com/ossf/scorecard) makes checks, supporting criteria, and remediation visible. [GrimoireLab](https://github.com/chaoss/grimoirelab) shows the value of project-level context for software maintenance. This toolkit applies those ideas to small, evidence-bound AI drafts with no repository write access.

## Adoption and maintenance plan

This is a new project and has no adoption metrics yet. We will earn adoption by making it easy to try on synthetic examples, documenting each input and output, and collecting sanitized failure cases from maintainers. Usage, external contributions, and release history will be reported only when they exist.

Near-term work:

1. Refine input schemas and human-readable output from maintainer feedback.
2. Add a documented evaluation set for prompt injection, unsupported claims, and secret handling before expanding automation.
3. Publish tagged releases with changelogs and compatibility notes once the interface settles.
4. Consider optional read-only GitHub adapters only if maintainers ask for them and the privacy model is clear. Any write capability would be separately designed and opt-in.
5. Review issues and contributions as capacity allows, use Dependabot to surface dependency and workflow updates, and update the security policy as maintainer capacity evolves.

See [ADOPTION.md](ADOPTION.md) for the honest impact baseline and measurement plan, and [CONTRIBUTING.md](CONTRIBUTING.md), [SUPPORT.md](SUPPORT.md), and [SECURITY.md](SECURITY.md) for community guidance. Open a feature request if a repeated maintainer task should become a workflow.

## License

MIT. See [LICENSE](LICENSE).
