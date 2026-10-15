"""Ultragent config schema.

Empty config and all-disabled method flags mean upstream Deep Agents parity.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MethodOption(BaseModel):
    """One named harness method flag.

    Attributes:
        enabled: Whether the option factory should emit artifacts. Default off.
        params: Opaque params forwarded to the registered option factory.
    """

    enabled: bool = False
    params: dict[str, object] = Field(default_factory=dict)


class UltragentConfig(BaseModel):
    """Top-level ultragent construction config.

    Attributes:
        methods: Named method options. Unknown ids are rejected at build time.
        profile_key: Optional harness profile key reserved for later pilots.
        backend: Backend id hint reserved for later pilots. Default is state.
    """

    methods: dict[str, MethodOption] = Field(default_factory=dict)
    profile_key: str | None = None
    backend: Literal["state", "filesystem", "composite"] = "state"
