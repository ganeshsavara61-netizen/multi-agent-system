import unittest

from multiagent import CalculatorAgent, Coordinator, Message, TextAgent


class CalculatorAgentTest(unittest.TestCase):
    def setUp(self):
        self.agent = CalculatorAgent()

    def test_handles_calculate_prefix(self):
        self.assertTrue(self.agent.can_handle(Message("user", "calculate: 1 + 1")))
        self.assertFalse(self.agent.can_handle(Message("user", "count: a b")))

    def test_calculates(self):
        reply = self.agent.handle(Message("user", "calculate: 6 * 7"))
        self.assertEqual(reply.content, "6 * 7 = 42")

    def test_rejects_unsafe_expression(self):
        reply = self.agent.handle(Message("user", "calculate: __import__('os')"))
        self.assertIn("could not calculate", reply.content)


class TextAgentTest(unittest.TestCase):
    def setUp(self):
        self.agent = TextAgent()

    def test_count(self):
        reply = self.agent.handle(Message("user", "count: one two three"))
        self.assertEqual(reply.content, "'one two three' has 3 words")

    def test_reverse(self):
        reply = self.agent.handle(Message("user", "reverse: abc"))
        self.assertEqual(reply.content, "cba")

    def test_upper(self):
        reply = self.agent.handle(Message("user", "upper: hi there"))
        self.assertEqual(reply.content, "HI THERE")


class CoordinatorTest(unittest.TestCase):
    def setUp(self):
        self.coordinator = Coordinator([CalculatorAgent(), TextAgent()])

    def test_routes_to_matching_agent(self):
        reply = self.coordinator.run("calculate: 2 ** 10")
        self.assertEqual(reply.sender, "calculator")
        self.assertEqual(reply.content, "2 ** 10 = 1024")

    def test_routes_text_task(self):
        reply = self.coordinator.run("count: a b c d")
        self.assertEqual(reply.sender, "text")

    def test_unhandled_task_returns_to_user(self):
        reply = self.coordinator.run("sing me a song")
        self.assertEqual(reply.sender, "user")

    def test_no_routing_loop(self):
        # An agent never receives a message it already handled.
        reply = self.coordinator.run("reverse: calculate: 1 + 1")
        self.assertEqual(reply.sender, "text")
        self.assertEqual(reply.content, "1 + 1 :etaluclac")

    def test_log_records_each_hop(self):
        self.coordinator.run("calculate: 1 + 2")
        senders = [m.sender for m in self.coordinator.log]
        self.assertEqual(senders, ["user", "calculator"])


if __name__ == "__main__":
    unittest.main()
