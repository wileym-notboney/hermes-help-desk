# Intake Contract Template

Copy this template into a deployment-specific design document. Replace bracketed values only after an operator approves them.

## Eligibility

- Accepted sender policy: `[explicit normalized allowlist or authenticated domain rule]`
- Unsupported input handling: ignore links and attachments during intake; record no untrusted instructions as policy.
- Canonical request identity: `[provider-specific immutable identity and normalization rule]`

## Ticket card

- Target ticket collection: `[configured immutable target]`
- Required properties:
  - `Task name`: concise, factual service-ticket title
  - `Status`: configured initial state
  - `Category`: `Service Ticket`
  - `Priority`: constrained allowed values
  - `Submitted by`: display name plus the claimed normalized sender email
  - `Notes`: factual summary and priority rationale
  - `URL`: blank unless a verified canonical source-thread URL exists

## Acknowledgement

- Exact content: `[approved fixed acknowledgement text]`
- Recipient: original normalized sender only
- Threading: original source thread only
- CC/BCC: empty
- Gate: confirmed ticket ID must be durably recorded first

## Recovery

- Create timeout or crash: enter a reconciliation queue; no automatic second create attempt.
- SMTP timeout or crash: enter a reconciliation queue; no automatic resend.
- Ledger retention and access: `[operator-approved policy]`
