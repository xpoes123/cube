"""Smoke test for the agent loop. Does NOT call the Anthropic API.

We exercise the bits we can without network: tool dispatch, schema
well-formedness, and FINAL_SOLUTION extraction.
"""

from __future__ import annotations

from cube.agent.loop import (
    TOOL_REGISTRY,
    _dispatch_tool,
    _extract_solution,
    _tool_schemas,
)


def test_all_tools_have_schemas():
    schemas = _tool_schemas()
    names = {s["name"] for s in schemas}
    assert names == set(TOOL_REGISTRY)
    # Anthropic requires name, description, input_schema on each tool.
    for s in schemas:
        assert "name" in s
        assert "description" in s
        assert "input_schema" in s
        assert s["input_schema"]["type"] == "object"


def test_dispatch_inspect_state_solved():
    out = _dispatch_tool("inspect_state", {"scramble": [], "history": []})
    assert out["is_solved"] is True
    assert out["move_count"] == 0


def test_dispatch_verify_solved_roundtrip():
    scramble = ["R", "U", "R'"]
    # Inverse solves it.
    out = _dispatch_tool(
        "verify_solved",
        {"scramble": scramble, "solution": ["R", "U'", "R'"]},
    )
    assert out["solves"] is True


def test_dispatch_try_alg_reports_delta():
    out = _dispatch_tool(
        "try_alg",
        {"scramble": ["R", "U", "R'"], "history": [], "alg": ["R", "U'", "R'"]},
    )
    assert out["solved"] is True


def test_dispatch_cancel():
    out = _dispatch_tool("cancel", {"moves": ["U", "U'"]})
    assert out["cancelled_moves"] == []
    assert out["saved"] == 2


def test_dispatch_invert():
    out = _dispatch_tool("invert", {"moves": ["R", "U", "R'"]})
    assert out["inverted"] == ["R", "U'", "R'"]


def test_dispatch_unknown_tool_returns_error():
    out = _dispatch_tool("nope", {})
    assert "error" in out


def test_dispatch_catches_exceptions():
    # Missing required key -> handler raises KeyError -> we return an error dict.
    out = _dispatch_tool("inspect_state", {})
    assert "error" in out


def test_extract_solution_simple():
    text = 'Looks good.\nFINAL_SOLUTION: ["R", "U", "R\'"]'
    assert _extract_solution(text) == ["R", "U", "R'"]


def test_extract_solution_case_insensitive():
    text = 'final_solution: ["U2", "D2"]'
    assert _extract_solution(text) == ["U2", "D2"]


def test_extract_solution_none_if_missing():
    assert _extract_solution("I'm thinking about it.") is None


def test_extract_solution_rejects_non_string_array():
    assert _extract_solution('FINAL_SOLUTION: [1, 2, 3]') is None
