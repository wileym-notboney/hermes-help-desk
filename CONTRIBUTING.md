# Contributing

Thanks for your interest in this project. It's an experimental, security-first reference blueprint, so contributions are especially welcome around correctness, safety, and clarity.

## Reporting bugs

Open a GitHub issue with:

- What you expected vs. what happened
- Steps to reproduce, ideally as a failing test
- Which workflow state(s) or file(s) are involved

For security vulnerabilities, see [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Submitting changes

1. Fork the repo and create a branch for your change.
2. Keep changes focused — one concern per pull request.
3. Add or update tests in `tests/` for any behavior change.
4. Run the test suite before opening a PR:
   ```
   python3 -m unittest discover -s tests -v
   ```
5. Open a pull request describing the change and why it's needed.

## Code style and conventions

- The `service_desk/` reference implementation is dependency-free — don't introduce external packages there.
- Keep the state machine's failure-closed behavior intact: no change should make an ambiguous outcome silently retry or double-send.
- Match existing code style within a file.

## Scope

This repo is a blueprint, not a turnkey integration — see the README's "Non-goals" section. Contributions that add a specific email/ticketing provider integration are likely out of scope; contributions that improve the reference state machine, docs, or contract templates are in scope.
