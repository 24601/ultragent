"""Factory parity and enable-path tests for create_ultragent."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from deepagents import create_deep_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from ultragent import MethodOption, UltragentConfig, create_ultragent
from ultragent.options.reflection_pass import ReflectionPassMiddleware


def _fake_chat_model() -> BaseChatModel:
    """Minimal chat model stand-in used by deepagents unit tests."""
    try:
        from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

        return GenericFakeChatModel(messages=iter([AIMessage(content="ok")]))
    except Exception:
        model = MagicMock(spec=BaseChatModel)
        model.model_name = "fake"
        return model


def _middleware_markers(middleware: list[Any]) -> list[str]:
    """Stack markers comparable to deepagents smoke naming."""
    markers: list[str] = []
    for item in middleware:
        name = getattr(item, "name", None)
        if isinstance(name, str) and name:
            markers.append(name)
            continue
        markers.append(type(item).__name__)
    return markers


def _capture_middleware(*, via_ultragent: bool = False, config: UltragentConfig | None = None) -> list[str]:
    """Construct an agent and return middleware stack markers."""
    captured: dict[str, list[Any]] = {}

    def _fake_create_agent(*_args: Any, **kwargs: Any) -> MagicMock:
        captured["middleware"] = list(kwargs.get("middleware") or [])
        agent = MagicMock()
        agent.with_config.return_value = agent
        return agent

    model = _fake_chat_model()
    with patch("deepagents.graph.create_agent", side_effect=_fake_create_agent):
        if via_ultragent:
            create_ultragent(model=model, config=config)
        else:
            create_deep_agent(model=model)

    assert "middleware" in captured
    return _middleware_markers(captured["middleware"])


def test_empty_config_middleware_parity() -> None:
    upstream = _capture_middleware()
    wrapped = _capture_middleware(via_ultragent=True, config=UltragentConfig())
    assert wrapped == upstream
    assert wrapped, "expected a non-empty middleware stack"


def test_all_disabled_config_middleware_parity() -> None:
    config = UltragentConfig(
        methods={
            "reflection_pass": MethodOption(enabled=False, params={"max_rounds": 1}),
        }
    )
    upstream = _capture_middleware()
    wrapped = _capture_middleware(via_ultragent=True, config=config)
    assert wrapped == upstream
    assert "ReflectionPassMiddleware" not in wrapped


def test_enabled_reflection_pass_appends_middleware() -> None:
    config = UltragentConfig(
        methods={
            "reflection_pass": MethodOption(enabled=True, params={"max_rounds": 2}),
        }
    )
    upstream = _capture_middleware()
    wrapped = _capture_middleware(via_ultragent=True, config=config)
    assert "ReflectionPassMiddleware" not in upstream
    assert "ReflectionPassMiddleware" in wrapped
    assert wrapped.count("ReflectionPassMiddleware") == 1
    filtered = [marker for marker in wrapped if marker != "ReflectionPassMiddleware"]
    assert filtered == upstream


def test_unknown_option_rejected() -> None:
    config = UltragentConfig(methods={"not_a_real_option": MethodOption(enabled=False)})
    with pytest.raises(ValueError, match="unknown ultragent option"):
        create_ultragent(model=_fake_chat_model(), config=config)


def test_reflection_pass_middleware_name() -> None:
    mw = ReflectionPassMiddleware(max_rounds=3)
    assert mw.name == "ReflectionPassMiddleware"
    assert mw.max_rounds == 3
