from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path
from typing import Any

from .workflows import WORKFLOWS, redact_context, validate_context


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _fingerprint(context: dict[str, Any]) -> str:
    canonical = json.dumps(context, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-reviewed OSS maintenance workflow drafts")
    parser.add_argument("workflow", choices=sorted(WORKFLOWS))
    parser.add_argument("input", type=Path, help="JSON context file")
    parser.add_argument("--send-to-openai", action="store_true", help="Explicitly send the previewed context to the OpenAI API")
    parser.add_argument("--confirm-context-sha256", help="Required with --send-to-openai; paste the fingerprint from a reviewed preview")
    parser.add_argument("--include-identifiers", action="store_true", help="Do not redact common identifiers (review the preview first)")
    parser.add_argument("--result-format", choices=("markdown", "json"), default="markdown", help="Format for the generated draft (default: markdown)")
    parser.add_argument("--output", type=Path, help="Optional local file for the generated draft")
    args = parser.parse_args()
    try:
        if args.input.stat().st_size > 500_000:
            raise ValueError("The JSON input file exceeds the 500 KB file-size limit.")
        context = json.loads(args.input.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        context = validate_context(args.workflow, context)
        redacted, count = redact_context(context)
        payload = context if args.include_identifiers else redacted
        fingerprint = _fingerprint(payload)
        print(f"Workflow: {args.workflow}")
        print(f"Common identifiers redacted: {0 if args.include_identifiers else count}")
        print("Context that would be sent (if --send-to-openai is used):")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print(f"Context SHA-256: {fingerprint}")
        if not args.send_to_openai:
            print("\nPreview only. Nothing was sent. Review this context, then add --send-to-openai and --confirm-context-sha256 with this fingerprint to make an API request.")
            return 0
        if not args.confirm_context_sha256:
            raise ValueError("API sending requires --confirm-context-sha256 with the fingerprint from a reviewed preview.")
        if not hmac.compare_digest(fingerprint, args.confirm_context_sha256.strip().lower()):
            raise ValueError("The context fingerprint does not match. Review the current preview and confirm its SHA-256 value.")
        print("\nReviewed context fingerprint confirmed; sending the API request.")
        if args.include_identifiers:
            print("\nIdentifiers are included by explicit request.", file=sys.stderr)
        from .api import run_workflow
        result = run_workflow(args.workflow, payload)
        if args.result_format == "markdown":
            from .render import render_markdown
            rendered = render_markdown(result)
        else:
            rendered = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(rendered + "\n", encoding="utf-8")
            print(f"\nDraft saved locally to {args.output}")
        print("\nDraft result:")
        print(rendered)
        print("\nReview this draft before using it. No GitHub changes were made.")
        return 0
    except (OSError, ValueError, RuntimeError, RecursionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
