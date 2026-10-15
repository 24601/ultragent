"""Option registry for ultragent method factories."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware

OptionFactory = Callable[[dict[str, object]], Sequence[AgentMiddleware[Any, Any, Any]]]

REGISTRY: dict[str, OptionFactory] = {}


def register_option(option_id: str, factory: OptionFactory) -> None:
    """Register a named option factory.

    Args:
        option_id: Stable method id used in `UltragentConfig.methods`.
        factory: Callable that turns params into middleware artifacts.

    Raises:
        ValueError: If `option_id` is already registered.
    """
    if option_id in REGISTRY:
        msg = f"duplicate option {option_id}"
        raise ValueError(msg)
    REGISTRY[option_id] = factory


def clear_registry() -> None:
    """Clear all registered options.

    Intended for tests that need an isolated registry.
    """
    REGISTRY.clear()
