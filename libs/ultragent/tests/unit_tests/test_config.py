"""Config schema defaults and validation."""

from ultragent.config import MethodOption, UltragentConfig


def test_method_option_defaults_off() -> None:
    option = MethodOption()
    assert option.enabled is False
    assert option.params == {}


def test_empty_ultragent_config() -> None:
    config = UltragentConfig()
    assert config.methods == {}
    assert config.profile_key is None
    assert config.backend == "state"


def test_method_option_round_trip() -> None:
    config = UltragentConfig(
        methods={
            "reflection_pass": MethodOption(enabled=True, params={"max_rounds": 2}),
        }
    )
    assert config.methods["reflection_pass"].enabled is True
    assert config.methods["reflection_pass"].params["max_rounds"] == 2
