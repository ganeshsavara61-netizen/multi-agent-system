"""A tiny multi-agent system: a coordinator routes tasks to specialized agents."""

from .message import Message
from .agents import Agent, CalculatorAgent, TextAgent
from .coordinator import Coordinator

__all__ = [
    "Message",
    "Agent",
    "CalculatorAgent",
    "TextAgent",
    "Coordinator",
]
