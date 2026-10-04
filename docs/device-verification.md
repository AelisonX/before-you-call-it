# Real-device verification

Date: 2026-10-04 (Australia/Brisbane).

Public position: **Tested on Windows 11.** Distribution remains a Windows-tested source-run prototype, with no unsigned executable distribution.

## Windows PC — completed publication evidence

The project owner reported completion of the following real-device checks:

- Windows 11 (previously recorded OS build: 10.0.26200).
- Interactive CLI flow completed.
- All five collectors exercised and returned expected observations.
- No unexpected privilege, privacy or security prompts: no UAC, privacy, Defender or SmartScreen prompts appeared.
- An actual disconnected-network run completed successfully; this is separate from the automated offline test.
- Network wording remained appropriately narrow and did not imply internet or company-service access.
- Public-safe screenshots captured. Screenshot files are not included in this repository.

The earlier local verification used source-run Python with psutil 7.2.2 in a project virtual environment; all 15 automated tests passed. No raw private measurements, identifiers or answers are stored here as evidence. These observations describe this tested Windows device and do not establish device health or enterprise readiness.

## macOS — CI compatibility evidence only

Windows and macOS CI pass on Python 3.10 and 3.13. CI is compatibility evidence only, not real-device support verification.

CI also runs on macOS, but no real macOS device verification has been completed, so macOS support is not currently claimed. Daniel's Mac is currently unavailable, so this verification remains pending.

When a Mac is available, record macOS and Python/psutil versions. Run as an ordinary user, answer with fictional data, try both opting out and opting in to collection, and run all tests. Review both previews, GiB labels, system-volume scope, uptime, network wording and omissions. Test while disconnected. Record unexpected output and public-safe screenshots. Confirm no privilege/privacy/security prompts; if any appear, STOP and review scope rather than bypassing them.

Neither Windows CI nor macOS CI substitutes for human device verification. No verified cross-platform support claim is made.
