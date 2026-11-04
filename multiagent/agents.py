"""Specialized agents. Each agent decides which tasks it can handle."""

import ast
import operator
from typing import Optional

from .message import Message


class Agent:
    """Base class: an agent has a name and handles messages."""

    name = "agent"

    def can_handle(self, message: Message) -> bool:
        raise NotImplementedError

    def handle(self, message: Message) -> Message:
        raise NotImplementedError


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def _safe_eval(node):
    """Evaluate an arithmetic AST node without using eval()."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _safe_eval(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("unsupported expression")


class CalculatorAgent(Agent):
    """Handles messages starting with 'calculate:'."""

    name = "calculator"

    def can_handle(self, message: Message) -> bool:
        return message.content.lower().startswith("calculate:")

    def handle(self, message: Message) -> Message:
        expression = message.content.split(":", 1)[1].strip()
        try:
            result = _safe_eval(ast.parse(expression, mode="eval"))
            reply = f"{expression} = {result}"
        except (ValueError, SyntaxError, ZeroDivisionError) as exc:
            reply = f"could not calculate '{expression}': {exc}"
        return Message(sender=self.name, content=reply,
                       history=message.history + [self.name])


class TextAgent(Agent):
    """Handles text tasks: 'count:', 'reverse:' and 'upper:'."""

    name = "text"

    def can_handle(self, message: Message) -> bool:
        lowered = message.content.lower()
        return lowered.startswith(("count:", "reverse:", "upper:"))

    def handle(self, message: Message) -> Message:
        command, _, rest = message.content.partition(":")
        text = rest.strip()
        command = command.strip().lower()
        if command == "count":
            reply = f"'{text}' has {len(text.split())} words"
        elif command == "reverse":
            reply = text[::-1]
        else:
            reply = text.upper()
        return Message(sender=self.name, content=reply,
                       history=message.history + [self.name])
