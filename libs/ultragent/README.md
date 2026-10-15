# ultragent

Thin config-first wrap around Deep Agents `create_deep_agent`.

This package is the ultragent extension shell. Method behavior lives here as
named options. `libs/deepagents/` stays an upstream-syncable core.

## Defaults

Empty config and all-disabled method flags build the same agent as stock
`create_deep_agent` for the same model kwargs. Options are default-off.

## Usage

```python
from ultragent import UltragentConfig, MethodOption, create_ultragent

# Upstream parity (empty config)
agent = create_ultragent(model="anthropic:claude-sonnet-4-6")

# Enable one registered option
config = UltragentConfig(
    methods={
        "reflection_pass": MethodOption(
            enabled=True,
            params={"max_rounds": 1},
        ),
    }
)
agent = create_ultragent(model="anthropic:claude-sonnet-4-6", config=config)
```

## Layout

- `config.py` - `UltragentConfig` / `MethodOption` schema
- `registry.py` - option id to factory map
- `factory.py` - `create_ultragent(...)`
- `options/` - one module per named method (default off)

## Sync intent

Treat `libs/deepagents/` as upstream. Land ultragent behavior only under
`libs/ultragent/`. Do not patch Deep Agents assembly for method work.

## Develop

```bash
cd libs/ultragent
uv sync --group test
make test
```
