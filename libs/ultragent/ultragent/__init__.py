"""Ultragent thin wrap around Deep Agents."""

from ultragent.config import MethodOption, UltragentConfig
from ultragent.factory import create_ultragent
from ultragent.registry import REGISTRY, register_option

# Import option modules so they self-register on package import.
from ultragent import options as _options  # noqa: F401

__all__ = [
    "REGISTRY",
    "MethodOption",
    "UltragentConfig",
    "create_ultragent",
    "register_option",
]

__version__ = "0.0.1"
