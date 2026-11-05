from __future__ import annotations

import argparse
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-reviewed OSS maintenance workflow drafts")
    parser.add_argument("workflow", choices=sorted(WORKFLOWS))
    parser.add_argument("input", type=Path, help="JSON context file")
    parser.add_argument("--send-to-openai", action="store_true", help="Explicitly send the previewed context to the OpenAI API")
    parser.add_argument("--include-identifiers", action="store_true", help="Do not redact common identifiers (review the preview first)")
    args = parser.parse_args()
    try:
        context = json.loads(args.input.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        context = validate_context(args.workflow, context)
        redacted, count = redact_context(context)
        payload = context if args.include_identifiers else redacted
        print(f"Workflow: {args.workflow}")
        print(f"Common identifiers redacted: {0 if args.include_identifiers else count}")
        print("Context that would be sent (if --send-to-openai is used):")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if not args.send_to_openai:
            print("\nPreview only. Nothing was sent. Add --send-to-openai to make an API request.")
            return 0
        if args.include_identifiers:
            print("\nIdentifiers are included by explicit request.", file=sys.stderr)
        from .api import run_workflow
        result = run_workflow(args.workflow, payload)
        print("\nDraft result:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\nReview this draft before using it. No GitHub changes were made.")
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
