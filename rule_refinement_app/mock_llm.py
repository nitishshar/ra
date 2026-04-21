"""Mock LLM responses for checkpoint evaluation and rule refinement."""

from __future__ import annotations

import random
import time
from typing import Any


def mock_checkpoint_evaluation(
    cde_name: str,
    cde_definition: str,
    rule_title: str,
    rule_dimension: str,
    business_text: str,
) -> dict[str, Any]:
    """Simulates an LLM checkpoint evaluation API call."""
    time.sleep(3)

    rule_absent = _is_rule_missing(business_text)
    evidence_prefix = (
        "No rule text provided — checkpoint evaluated against CDE definition only."
        if rule_absent
        else f"The rule business text states '{business_text[:60]}...'"
    )

    checkpoints = [
        {
            "checkpoint_key": "DQ Dimension Mapping",
            "outcome": "pass" if not rule_absent else "fail",
            "notes": (
                f"The rule correctly maps to the {rule_dimension} dimension as it checks "
                "for the correctness of the data element."
            ) if not rule_absent else (
                f"No rule text provided. Cannot verify dimension mapping to {rule_dimension}."
            ),
            "evidence": evidence_prefix,
        },
        {
            "checkpoint_key": "DQ Dimension Coverage Consistency",
            "outcome": "pass",
            "notes": (
                f"The rule consistently applies to the {rule_dimension} dimension without "
                "mixing with other dimensions."
            ),
            "evidence": (
                f"The rule only checks for the correctness of the {cde_name}, which is a "
                "single dimension concern."
            ),
        },
        {
            "checkpoint_key": "Data Element Context",
            "outcome": "pass",
            "notes": (
                f"The rule correctly references and aligns with the Data Element Context of "
                f"the {cde_name}."
            ),
            "evidence": (
                f"The rule uses the {cde_name} to identify the counterparty context correctly."
            ),
        },
        {
            "checkpoint_key": "Dimension Applicability",
            "outcome": "pass",
            "notes": (
                f"The rule is only evaluated against checkpoints applicable to the declared "
                f"dimension ({rule_dimension})."
            ),
            "evidence": (
                f"The evaluation only considers checkpoints with Dimension = '{rule_dimension}' "
                "or 'All'."
            ),
        },
        {
            "checkpoint_key": "Check for Dimension Mixing",
            "outcome": random.choice(["pass", "pass", "fail"]),
            "notes": "The rule does not mix multiple distinct dimensions.",
            "evidence": f"The rule only addresses the {rule_dimension} dimension.",
        },
    ]

    passed = sum(1 for c in checkpoints if c["outcome"] == "pass")
    failed = len(checkpoints) - passed

    return {
        "checkpoint_evaluation": {
            "checkpoint_results": checkpoints,
            "dimension_analysis": {
                "detected_dimensions": [rule_dimension],
                "should_split": False,
                "split_reason": (
                    f"The rule only addresses a single dimension ({rule_dimension}) and does "
                    "not require splitting."
                ),
            },
            "summary": {
                "total_checkpoints": len(checkpoints),
                "passed": passed,
                "failed": failed,
                "warnings": 0,
                "skipped": 0,
            },
        }
    }


def _is_rule_missing(business_text: str) -> bool:
    """Return True when no meaningful rule text has been provided."""
    normalized = business_text.strip().upper()
    return normalized in ("", "TBD", "N/A", "NONE", "-")


def mock_rule_refinement(
    original_rule: dict[str, str],
    checkpoint_results: dict[str, Any],
) -> dict[str, Any]:
    """Simulates an LLM rule refinement API call.

    When business_text is absent or TBD, returns a generated ``suggested_rule``
    instead of an ``improved_business_text``.
    """
    _ = checkpoint_results
    time.sleep(2)

    business_text = original_rule["business_text"]
    cde_name = original_rule["cde_name"]
    cde_definition = original_rule.get("cde_definition", "")
    rule_dimension = original_rule.get("rule_dimension", "Accuracy")

    if _is_rule_missing(business_text):
        return {
            "rule_refinement": {
                "improved_business_text": None,
                "suggested_rule": {
                    "business_text": (
                        f"Produce error if {cde_name} is null, empty, or does not conform to "
                        f"the expected format as defined in the data dictionary. "
                        f"All active records must carry a valid {cde_name} value."
                    ),
                    "dimension": rule_dimension,
                    "rationale": (
                        f"No business rule was provided for {cde_name}. Based on its definition "
                        f"(\"{cde_definition}\") and the declared {rule_dimension} dimension, "
                        f"this rule was generated to enforce baseline data quality expectations."
                    ),
                    "note": (
                        "This is an AI-generated suggestion. Please review and validate against "
                        "business requirements before promoting to production."
                    ),
                },
                "rationale": (
                    f"Rule text was not provided (value: \"{business_text.strip() or 'empty'}\"). "
                    f"A new rule was generated from the CDE definition and declared dimension."
                ),
                "key_changes": [
                    f"No existing rule — generated from scratch for '{cde_name}'",
                    f"Dimension set to '{rule_dimension}' as declared on the element",
                    "Null/empty check and format validation included as baseline conditions",
                    "Review note added: AI-generated output requires human validation",
                ],
                "split_recommended": False,
                "split_rules": [],
            }
        }

    return {
        "rule_refinement": {
            "improved_business_text": (
                f"Produce error if the {cde_name} value is invalid or does not meet the "
                f"expected format when the associated counterparty record is active and present "
                f"in the registry. Original condition: {business_text}"
            ),
            "suggested_rule": None,
            "rationale": (
                f"This rule is important for data quality and business operations as it ensures "
                f"that the {cde_name} field maintains accuracy standards. The refined version adds "
                "explicit reference to active record context for clarity."
            ),
            "key_changes": [
                f"Added explicit reference to the CDE name '{cde_name}' for clarity and context",
                "Clarified the condition to include active record constraint",
                "Improved readability while preserving the original business logic",
            ],
            "split_recommended": False,
            "split_rules": [],
        }
    }
