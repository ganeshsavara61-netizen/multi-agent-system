# Multi-Agent System

A small multi-agent system in plain Python. A coordinator acts as a message
bus and routes tasks to specialized agents; each agent handles the tasks it
recognizes and passes its reply back to the bus.

This is a **learning project**. The agents are rule-based (no AI model, no
external APIs, no third-party packages). A model-backed agent can be added
later by implementing the same `Agent` interface.

## How it works

- `multiagent/message.py` - the `Message` dataclass that travels through the
  system. It tracks which agents already handled it, so routing cannot loop.
- `multiagent/agents.py` - the `Agent` base class plus two agents:
  - `CalculatorAgent` answers `calculate: <expression>` using a safe AST
    evaluator (no `eval`).
  - `TextAgent` answers `count:`, `reverse:` and `upper:` text tasks.
- `multiagent/coordinator.py` - the `Coordinator`. For each message it picks
  the first agent that can handle it and has not handled it yet, then feeds
  the reply back into the bus until no agent can take the next step.

## Quick start

```bash
python main.py
```

Example output:

```
task:   calculate: 6 * 7
route:  user -> calculator
result: 6 * 7 = 42
```

Run your own task:

```bash
python main.py "count: multi agent systems route tasks"
```

## Tests

```bash
python -m unittest discover -s tests
```

## Status

Tested with Python 3.10. No extra packages.

## Next steps

- Add a model-backed agent behind the same `Agent` interface.
- Let agents talk to each other, not only to the coordinator.
- Add async message handling.
