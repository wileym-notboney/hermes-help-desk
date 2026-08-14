# Hermes Help Desk Blueprint

> **Experimental reference implementation — not production-ready.**

A security-first blueprint for turning one eligible inbound email into one service-ticket card and, only after that card is confirmed, one constrained acknowledgement. It is designed to make unsafe retries fail closed rather than silently create duplicate tickets or acknowledgements.

This repository contains architecture, templates, and a small dependency-free state-machine reference. It does **not** contain email credentials, OAuth tokens, data-source identifiers, real messages, customer information, hostnames, deployed configuration, or a turnkey production integration.

## Why this exists

This started as a way to help manage tech support for family members who've had a harder time keeping up with new technology. Casual back-and-forth troubleshooting — texts, calls, drop-ins — was becoming a source of friction rather than help, and the existing help-desk tools were either too technical to hand off or too heavyweight to justify for a household. Since Hermes can already ingest email, a dedicated help account routed through Hermes into a Kanban board seemed like the natural fix: reports land as tickets I can triage on my own schedule, instead of pings I have to catch in real time.

Full disclosure: I've been lurking in open source for ages without ever putting anything out there myself. This is my first public project, so go easy on the rough edges — feedback and PRs are welcome.

Building that meant treating email-to-ticket automation like the risky system it is. It combines three risky boundaries:

1. **Untrusted input:** email bodies, headers, links, quoted replies, and attachments may be attacker controlled.
2. **External writes:** ticket creation and acknowledgement delivery have user-visible consequences.
3. **Failure windows:** an email API, ticket API, database, or SMTP service can fail after accepting work but before the workflow records success.

The intended posture is conservative: create at most one ticket attempt per durable request identity, require confirmed ticket creation before acknowledgement, and require manual reconciliation after ambiguous external outcomes.

## Workflow contract

```text
RECEIVED
  -> PROCESSING
  -> TICKET_CREATING
  -> TICKET_CREATED
  -> ACK_SENDING
  -> COMPLETE

ACK_SENDING -> FAILED_AFTER_TICKET
```

- `TICKET_CREATING` is entered atomically before the single ticket-create attempt.
- `TICKET_CREATED` requires a confirmed created-ticket identifier.
- `ACK_SENDING` is persisted before SMTP begins.
- `FAILED_AFTER_TICKET` is terminal in this reference: reconcile it; do not blindly resend.

See [docs/architecture.md](docs/architecture.md) for boundaries and [templates/intake-contract.md](templates/intake-contract.md) for a deployment-neutral contract.

## Quick start

```text
python3 -m unittest discover -s tests -v
```

The test suite exercises the reference state machine only. It makes no network calls.

## What an implementation must provide

- A provider-appropriate, normalized durable request identity.
- An atomic durable claim before any ticket side effect.
- A fixed target ticket collection and allowlisted sender policy.
- A strict ticket property contract, including submitter binding.
- Confirmed ticket ID recording before an acknowledgement attempt.
- Exact acknowledgement text, original-thread behavior, normalized sender-only recipient, and empty CC/BCC.
- A reconciliation process for ambiguous create and SMTP outcomes.

## Non-goals

- A plug-and-play Gmail, IMAP, SMTP, Notion, or Hermes deployment.
- Automatic interpretation of attachments or email links.
- “Exactly once” claims across independent external services.
- Autonomous retries after an ambiguous ticket or acknowledgement outcome.

## Current experimental limitations

This blueprint is intentionally honest about unfinished production work:

- It does not prove an externally atomic create-and-record operation.
- It does not ship a connector adapter or OAuth flow.
- It does not choose an identity model for every mail provider.
- It does not replace a security review, retention policy, or operator runbook.

## Repository layout

```text
service_desk/          Dependency-free reference state machine
tests/                 Local behavior tests
docs/                  Threat model and architecture
templates/             Deployment-neutral contracts
```

## License

MIT. See [LICENSE](LICENSE).
