# Architecture and Threat Model

## Trust boundary

Treat every inbound email component as untrusted data:

- sender display name and address;
- headers and quoted reply chains;
- subject and body;
- links, tracking pixels, and attachments.

An intake worker must not follow embedded instructions that request configuration changes, different ticket targets, policy exceptions, credential access, or new acknowledgement wording.

## Required boundaries

| Boundary | Required control |
|---|---|
| Eligibility | Normalize and allowlist the original sender before processing. |
| Identity | Claim a provider-appropriate durable request identity atomically. |
| Ticket target | Permit exactly one configured ticket collection. |
| Card shape | Validate an exact property allowlist and bind `Submitted by` to the claimed sender. |
| Acknowledgement | Require confirmed ticket creation, exact content, sender-only recipient, original thread, and empty CC/BCC. |
| Recovery | Treat ambiguous external outcomes as reconciliation cases, not retries. |

## State semantics

### `PROCESSING`

A durable identity has been claimed. No ticket request is authorized until the workflow moves to `TICKET_CREATING`.

### `TICKET_CREATING`

The workflow authorized one ticket-create call. A crash or timeout here is ambiguous: the ticket system may have accepted the request. Block further create attempts and reconcile using an implementation-specific correlation strategy.

### `TICKET_CREATED`

A ticket API response was validated and its created-ticket identifier was durably recorded. Only acknowledgement recovery is permitted from this state.

### `ACK_SENDING`

The acknowledgement attempt began. SMTP acceptance may be uncertain after a timeout, so do not blindly resend.

### Terminal states

- `COMPLETE`: ticket and acknowledgement acceptance were durably recorded.
- `FAILED_AFTER_TICKET`: ticket exists or may exist, but acknowledgement requires operator reconciliation.

## Recommended reconciliation design

Choose a correlation value that can be stored and searched in the ticket system without exposing unnecessary personal data. Before any recovery from `TICKET_CREATING`, search for the correlated ticket and record its verified identifier if found. If correlation cannot prove the result, escalate to an operator rather than creating another ticket.

## Privacy posture

Keep the durable ledger minimal: identity, normalized sender, state, external IDs, timestamps, and bounded failure reason. Encrypt or otherwise protect it according to the deployment environment. Do not publish ledger contents, real inbox data, OAuth material, or production identifiers.
