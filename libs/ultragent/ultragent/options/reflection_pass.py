"""Stub reflection_pass option.

Default off. Emits one ReflectionPassMiddleware when enabled.
No measured behavior claim. Measurement belongs in a later pilot unit.
"""

from __future__ import annotations

from typing import Any

from langchain.agents.middleware.types import AgentMiddleware

from ultragent.registry import register_option

OPTION_ID = "reflection_pass"


class ReflectionPassMiddleware(AgentMiddleware[Any, Any, Any]):
    """Placeholder reflection middleware for registry wiring tests."""

    name = "ReflectionPassMiddleware"

    def __init__(self, max_rounds: int = 1) -> None:
        """Store reflection round budget.

        Args:
            max_rounds: Max reflection rounds when behavior is implemented.
        """
        super().__init__()
        self.max_rounds = max_rounds


def build(params: dict[str, object]) -> list[AgentMiddleware[Any, Any, Any]]:
    """Build middleware for reflection_pass.

    Args:
        params: Option params. Recognizes `max_rounds` (default 1).

    Returns:
        A single ReflectionPassMiddleware instance.
    """
    max_rounds = int(params.get("max_rounds", 1))  # type: ignore[arg-type]
    return [ReflectionPassMiddleware(max_rounds=max_rounds)]


register_option(OPTION_ID, build)
