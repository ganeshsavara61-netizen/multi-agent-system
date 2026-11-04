"""Messages passed between the coordinator and agents."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Message:
    """A single unit of work moving through the system.

    sender:  name of the agent (or "user") that produced the message.
    content: the task text or a result.
    history: names of agents that have already handled this message,
             used to prevent routing loops.
    """

    sender: str
    content: str
    history: List[str] = field(default_factory=list)
