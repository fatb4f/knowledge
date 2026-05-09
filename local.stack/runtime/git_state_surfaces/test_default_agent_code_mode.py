import json

from state_acp import state_hydrate_acp
from state_core import render_response
from state_mcp import state_get_mcp

def test_core_get_state_response_is_json() -> None:
    rendered = render_response(operation="get_state", backend="gix", encoding="json")
    payload = json.loads(rendered)
    assert payload["kind"] == "response"
    assert payload["operation"] == "get_state"
    assert payload["backend"] == "gix"
    assert payload["runtime"]["host"] == "marimo"
    assert payload["payload"]["schema_version"] == "state.v1"
    assert payload["session"]["host"] == "marimo"
    assert payload["encoding"] == "json"
    assert payload["output"]["encoding"] == "json"


def test_core_hydrate_state_response_is_ndjson_line() -> None:
    rendered = render_response(operation="hydrate_state", backend="gix", encoding="ndjson")
    lines = rendered.strip().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["operation"] == "hydrate_state"
    assert payload["encoding"] == "ndjson"
    assert payload["payload"]["schema_version"] == "state.v1"
    assert payload["output"]["encoding"] == "ndjson"
    assert payload["output"]["streaming"] is True


def test_mcp_binding_sets_transport() -> None:
    rendered = state_get_mcp(backend="gix", encoding="json")
    payload = json.loads(rendered)
    assert payload["transport"] == "mcp"
    assert payload["session"]["transport"] == "mcp"
    assert payload["operation"] == "get_state"


def test_acp_binding_sets_transport() -> None:
    rendered = state_hydrate_acp(backend="gix", encoding="json")
    payload = json.loads(rendered)
    assert payload["transport"] == "acp"
    assert payload["session"]["transport"] == "acp"
    assert payload["operation"] == "hydrate_state"
