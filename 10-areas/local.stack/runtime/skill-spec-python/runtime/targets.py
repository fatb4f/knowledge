from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Artifact = Literal["state", "session", "output"]


@dataclass
class RuntimeIngress:
    artifact: Artifact
    payload: dict[str, Any] = field(default_factory=dict)
    reject_unknown_keys: bool = True
