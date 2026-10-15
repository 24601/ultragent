"""Factory that wraps `create_deep_agent` with ultragent options."""

from __future__ import annotations

from typing import Any

from deepagents import create_deep_agent
from langchain_core.language_models import BaseChatModel

from ultragent.config import UltragentConfig
from ultragent.registry import REGISTRY


def create_ultragent(
    model: str | BaseChatModel | None = None,
    *,
    config: UltragentConfig | None = None,
    **kwargs: Any,
) -> Any:
    """Create an agent via Deep Agents with optional ultragent method flags.

    Empty config or all-disabled options pass through to `create_deep_agent`
    with no extra middleware. Enabled options append registered middleware
    after any caller-supplied middleware.

    Args:
        model: Model string or chat model instance forwarded upstream.
        config: Ultragent config. Defaults to empty (upstream parity).
        **kwargs: Remaining kwargs forwarded to `create_deep_agent`.

    Returns:
        Compiled Deep Agents graph from `create_deep_agent`.

    Raises:
        ValueError: If config references an unknown option id.
    """
    resolved = config or UltragentConfig()
    extra_middleware: list[Any] = []
    for option_id, option in resolved.methods.items():
        if option_id not in REGISTRY:
            msg = f"unknown ultragent option {option_id!r}"
            raise ValueError(msg)
        if not option.enabled:
            continue
        extra_middleware.extend(REGISTRY[option_id](option.params))

    existing = list(kwargs.pop("middleware", ()) or ())
    return create_deep_agent(
        model=model,
        middleware=[*existing, *extra_middleware],
        **kwargs,
    )
