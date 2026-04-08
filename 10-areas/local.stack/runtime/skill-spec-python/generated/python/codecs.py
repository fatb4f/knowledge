from __future__ import annotations

import json
from typing import Any

import msgspec


json_encoder = msgspec.json.Encoder()


def encode_json(value: Any) -> bytes:
    return json_encoder.encode(value)


def encode_jsonl(values: list[Any]) -> bytes:
    return b"".join(json_encoder.encode(value) + b"\n" for value in values)


def pretty_json(value: Any) -> str:
    return json.dumps(msgspec.to_builtins(value), indent=2, sort_keys=True)
