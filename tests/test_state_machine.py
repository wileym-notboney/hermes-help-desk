"""Behavior tests for the public reference workflow."""
import unittest

from service_desk.state_machine import State, TransitionError, Workflow


class WorkflowTests(unittest.TestCase):
    def test_happy_path_requires_create_then_acknowledgement(self):
        flow = Workflow()
        self.assertEqual(flow.state, State.RECEIVED)
        flow.claim()
        flow.authorize_ticket_create()
        flow.record_ticket_created("page-demo-001")
        flow.begin_acknowledgement()
        flow.record_acknowledgement_accepted("message-demo-001")
        self.assertEqual(flow.state, State.COMPLETE)

    def test_duplicate_or_ambiguous_create_never_authorizes_second_card(self):
        flow = Workflow()
        flow.claim()
        flow.authorize_ticket_create()
        with self.assertRaises(TransitionError):
            flow.authorize_ticket_create()
        with self.assertRaises(TransitionError):
            flow.begin_acknowledgement()

    def test_failed_acknowledgement_is_terminal_and_requires_reconciliation(self):
        flow = Workflow()
        flow.claim()
        flow.authorize_ticket_create()
        flow.record_ticket_created("page-demo-001")
        flow.begin_acknowledgement()
        flow.record_acknowledgement_failure("timeout")
        self.assertEqual(flow.state, State.FAILED_AFTER_TICKET)
        with self.assertRaises(TransitionError):
            flow.begin_acknowledgement()

    def test_ticket_cannot_be_recorded_without_a_page_identifier(self):
        flow = Workflow()
        flow.claim()
        flow.authorize_ticket_create()
        with self.assertRaises(ValueError):
            flow.record_ticket_created("")


if __name__ == "__main__":
    unittest.main()
