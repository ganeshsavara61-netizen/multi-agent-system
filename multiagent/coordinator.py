"""The coordinator routes messages between agents until a task is done."""

from typing import Iterable, List, Optional

from .agents import Agent
from .message import Message


class Coordinator:
    """A minimal message bus.

    The coordinator keeps a list of agents. For each incoming message it
    picks the first agent that (a) can handle it and (b) has not handled
    this message yet, then feeds the agent's reply back into the bus.
    A task is done when no agent can take the next step.
    """

    def __init__(self, agents: Iterable[Agent], max_steps: int = 10):
        self.agents: List[Agent] = list(agents)
        self.max_steps = max_steps
        self.log: List[Message] = []

    def _next_agent(self, message: Message) -> Optional[Agent]:
        for agent in self.agents:
            if agent.name in message.history:
                continue
            if agent.can_handle(message):
                return agent
        return None

    def run(self, task: str) -> Message:
        """Run one task through the agent network and return the final reply."""
        message = Message(sender="user", content=task)
        self.log.append(message)
        for _ in range(self.max_steps):
            agent = self._next_agent(message)
            if agent is None:
                return message
            message = agent.handle(message)
            self.log.append(message)
        raise RuntimeError("max routing steps exceeded (possible loop)")
