# Real-device verification

Date: 2026-10-04 (Australia/Brisbane).

## Windows PC — partial verification

- Windows 11, OS build 10.0.26200.
- Source-run Python with psutil 7.2.2 in a project virtual environment.
- 15 automated tests passed on the user's Windows host.
- All five live collectors returned OBSERVED.
- No collector raised a permission denial. CLI preview was exercised with fictional answers.
- No raw private measurements, identifiers or answers are stored as evidence.
- Remaining: human interactive review, screenshots of fictional previews, confirmation of no visible OS privacy/privilege prompts, unexpected-output notes, and actual disconnected-network run. The offline unit test blocks socket connect; it is not a physical disconnected-device test.

## Daniel's Mac — not tested

Record macOS version and Python/psutil versions. Run as an ordinary user, answer with fictional data, try both opting out and opting in to collection, and run all tests. Review both previews, GiB labels, system-volume scope, uptime, network wording and omissions. Test while disconnected. Record unexpected output and screenshots without identifiers. Confirm no privilege/privacy prompts; if any appear, STOP and review scope rather than bypassing them.

CI evidence is separate from this real-device checklist. Neither Windows CI nor macOS CI substitutes for human device verification.
