from __future__ import annotations

import copy
import unittest

from app.output_guard import guard_output


RULES = {
    "required_fields": ["answer", "status", "evidence", "risk_flags", "next_action"],
    "allowed_statuses": ["supported", "partial", "unsupported"],
    "allowed_next_actions": ["answer_user", "ask_clarifying_question", "refuse"],
    "allowed_risk_flags": ["missing_data", "unsafe_source", "prompt_injection", "unsupported_claim", "none"],
    "require_evidence_for_statuses": ["supported", "partial"],
    "require_source_exists": True,
    "require_source_in_context": True,
    "require_quote_exact_match": True,
    "minimum_quote_length": 12,
    "unsupported_disallowed_actions": ["answer_user"],
    "check_expected_status": True,
    "check_expected_next_action": True,
}

SOURCES = {
    "D1_current_quiz_scope": {
        "source_id": "D1_current_quiz_scope",
        "content": "Quiz 2 obejmuje dokladnie dwa tematy: petle `while` oraz list comprehensions.",
    },
    "D2_teacher_email": {
        "source_id": "D2_teacher_email",
        "content": "Aktualne tematy to petle `while` oraz list comprehensions.",
    },
}

BASE_TRACE = {
    "case_id": "c1_supported_quiz_scope",
    "expected_status": "supported",
    "expected_next_action": "answer_user",
    "context_sources": [SOURCES["D1_current_quiz_scope"]],
    "parse_error": None,
    "parsed_output": {
        "status": "supported",
        "answer": "Quiz 2 obejmuje petle while oraz list comprehensions.",
        "evidence": [
            {
                "claim": "Quiz 2 obejmuje petle while oraz list comprehensions.",
                "source_id": "D1_current_quiz_scope",
                "quote": "Quiz 2 obejmuje dokladnie dwa tematy: petle `while` oraz list comprehensions.",
            }
        ],
        "risk_flags": ["none"],
        "next_action": "answer_user",
    },
}


def check_by_id(result: dict, check_id: str) -> dict:
    for check in result["checks"]:
        if check["id"] == check_id:
            return check
    raise AssertionError(f"Missing check: {check_id}")


class OutputGuardTests(unittest.TestCase):
    def test_valid_supported_trace_passes(self) -> None:
        result = guard_output(copy.deepcopy(BASE_TRACE), RULES, SOURCES)
        self.assertTrue(result["overall_passed"])

    def test_missing_required_field_fails(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        del trace["parsed_output"]["answer"]

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "required_field.answer")["passed"])
        self.assertFalse(result["overall_passed"])

    def test_unknown_status_fails(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        trace["parsed_output"]["status"] = "certain"

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "status_allowed")["passed"])
        self.assertFalse(result["overall_passed"])

    def test_unknown_next_action_fails(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        trace["parsed_output"]["next_action"] = "send_email"

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "next_action_allowed")["passed"])
        self.assertFalse(result["overall_passed"])

    def test_source_id_must_exist_in_catalog(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        trace["parsed_output"]["evidence"][0]["source_id"] = "D404_missing"

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "evidence[0].source_exists")["passed"])
        self.assertFalse(result["overall_passed"])

    def test_source_id_must_be_in_context_not_only_in_catalog(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        trace["parsed_output"]["evidence"][0]["source_id"] = "D2_teacher_email"
        trace["parsed_output"]["evidence"][0]["quote"] = "Aktualne tematy to petle `while` oraz list comprehensions."

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "evidence[0].source_in_context")["passed"])
        self.assertFalse(result["overall_passed"])

    def test_quote_must_be_exact_fragment_of_cited_source(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        trace["parsed_output"]["evidence"][0]["quote"] = "Quiz 2 obejmuje petle while i list comprehensions."

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "evidence[0].quote_exact_match")["passed"])
        self.assertFalse(result["overall_passed"])

    def test_unsupported_answer_cannot_be_sent_as_normal_answer(self) -> None:
        trace = copy.deepcopy(BASE_TRACE)
        trace["expected_status"] = "unsupported"
        trace["expected_next_action"] = "ask_clarifying_question"
        trace["parsed_output"] = {
            "status": "unsupported",
            "answer": "Nie ma danych o czasie quizu, ale pewnie potrwa 20 minut.",
            "evidence": [],
            "risk_flags": ["missing_data"],
            "next_action": "answer_user",
        }

        result = guard_output(trace, RULES, SOURCES)

        self.assertFalse(check_by_id(result, "unsupported_next_action_policy")["passed"])
        self.assertFalse(result["overall_passed"])


if __name__ == "__main__":
    unittest.main()
