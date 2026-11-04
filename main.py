"""Demo: run a few tasks through the multi-agent system.

Usage:
    python main.py                 # run the built-in demo tasks
    python main.py "count: one two three"
"""

import sys

from multiagent import CalculatorAgent, Coordinator, TextAgent


def build_coordinator() -> Coordinator:
    return Coordinator([CalculatorAgent(), TextAgent()])


def run_tasks(tasks):
    coordinator = build_coordinator()
    for task in tasks:
        final = coordinator.run(task)
        route = " -> ".join(m.sender for m in coordinator.log)
        print(f"task:   {task}")
        print(f"route:  {route}")
        print(f"result: {final.content}")
        print()
        coordinator.log.clear()


if __name__ == "__main__":
    demo_tasks = sys.argv[1:] or [
        "calculate: 6 * 7",
        "count: multi agent systems route tasks",
        "reverse: hello agents",
        "upper: done",
    ]
    run_tasks(demo_tasks)
