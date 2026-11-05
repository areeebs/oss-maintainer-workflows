"""Human-readable rendering for locally reviewable workflow drafts."""
from __future__ import annotations

import html
from typing import Any


def _quote(value: str) -> str:
    safe = html.escape(value, quote=False)
    return "\n".join("> " + line for line in safe.splitlines()) or ">"


def render_markdown(result: dict[str, Any]) -> str:
    lines = [f"# {result['workflow'].replace('-', ' ').title()} draft", "",
             f"**Priority:** {result['priority']}  ",
             f"**Confidence:** {result['confidence']}", "", "## Summary", "",
             _quote(result["summary"]), "", "## Findings", ""]
    if result["findings"]:
        for finding in result["findings"]:
            lines.extend([f"### {html.escape(finding['severity'].title())}: {html.escape(finding['title'])}", "",
                          "**Evidence from supplied context:**", "", _quote(finding["evidence"]), "",
                          "**Suggested action:**", "", _quote(finding["recommendation"]), ""])
    else:
        lines.extend(["No supported findings were returned.", ""])
    lines.extend(["## Evidence gaps", ""])
    lines.extend([f"- {html.escape(item)}" for item in result["evidence_gaps"]] or ["- None reported."])
    lines.extend(["", "## Suggested next steps", ""])
    lines.extend([f"- {html.escape(item)}" for item in result["next_steps"]] or ["- None suggested."])
    lines.extend(["", "## Draft text", "", _quote(result["draft"]), "",
                  "---", "Review all claims and project policy before use. This is an AI-generated draft.", ""])
    return "\n".join(lines)
