"""Option registry registration rules."""

import pytest

from ultragent.options.reflection_pass import OPTION_ID, build
from ultragent.registry import REGISTRY, register_option


def test_reflection_pass_self_registers_on_import() -> None:
    assert OPTION_ID in REGISTRY
    assert REGISTRY[OPTION_ID] is build


def test_duplicate_registration_raises() -> None:
    option_id = "tmp_duplicate_probe"
    register_option(option_id, build)
    try:
        with pytest.raises(ValueError, match="duplicate option tmp_duplicate_probe"):
            register_option(option_id, build)
    finally:
        del REGISTRY[option_id]
