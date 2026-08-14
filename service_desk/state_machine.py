"""A dependency-free, fail-closed reference state machine.

This module demonstrates workflow policy only. It does not fetch email, call
Notion, send acknowledgements, store credentials, or provide an exactly-once
distributed transaction.
"""
from __future__ import annotations

from enum import Enum


class State(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    TICKET_CREATING = "TICKET_CREATING"
    TICKET_CREATED = "TICKET_CREATED"
    ACK_SENDING = "ACK_SENDING"
    COMPLETE = "COMPLETE"
    FAILED_AFTER_TICKET = "FAILED_AFTER_TICKET"


class TransitionError(RuntimeError):
    """Raised when an unsafe or duplicate workflow transition is requested."""


class Workflow:
    """Reference policy for one inbound request and one ticket attempt."""

    def __init__(self) -> None:
        self.state = State.RECEIVED
        self.ticket_id: str | None = None
        self.acknowledgement_id: str | None = None
        self.failure_reason: str | None = None

    def _require(self, expected: State) -> None:
        if self.state is not expected:
            raise TransitionError(
                f"expected {expected.value}, found {self.state.value}"
            )

    def claim(self) -> None:
        self._require(State.RECEIVED)
        self.state = State.PROCESSING

    def authorize_ticket_create(self) -> None:
        """Enter a fail-closed state before the sole external ticket attempt."""
        self._require(State.PROCESSING)
        self.state = State.TICKET_CREATING

    def record_ticket_created(self, ticket_id: str) -> None:
        self._require(State.TICKET_CREATING)
        if not isinstance(ticket_id, str) or not ticket_id.strip():
            raise ValueError("a confirmed ticket identifier is required")
        self.ticket_id = ticket_id.strip()
        self.state = State.TICKET_CREATED

    def begin_acknowledgement(self) -> None:
        self._require(State.TICKET_CREATED)
        self.state = State.ACK_SENDING

    def record_acknowledgement_accepted(self, acknowledgement_id: str) -> None:
        self._require(State.ACK_SENDING)
        if not isinstance(acknowledgement_id, str) or not acknowledgement_id.strip():
            raise ValueError("an accepted acknowledgement identifier is required")
        self.acknowledgement_id = acknowledgement_id.strip()
        self.state = State.COMPLETE

    def record_acknowledgement_failure(self, reason: str) -> None:
        self._require(State.ACK_SENDING)
        self.failure_reason = str(reason or "unknown acknowledgement failure")
        self.state = State.FAILED_AFTER_TICKET
