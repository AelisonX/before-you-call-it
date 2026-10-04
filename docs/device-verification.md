# Real-device verification

Date: 2026-10-04 (Australia/Brisbane).

Public position: **Tested on Windows 11.** Distribution remains a Windows-tested source-run prototype, with no unsigned executable distribution. The corrected build still needs a physical disconnected-network rerun; it is not yet publication-ready.

## Windows PC — earlier publication evidence

The project owner reported completion on Windows 11 (previously recorded OS build: 10.0.26200):

- Interactive CLI flow completed; the original five collectors were exercised.
- No UAC, privacy, Defender or SmartScreen prompts appeared.
- An actual disconnected-network run completed successfully.
- Public-safe screenshots were captured; files are not included in this repository.

The earlier physical disconnected-network run produced “A network interface appears available.” Post-build review found this could be satisfied by loopback or virtual interfaces, so it was not useful enough to retain. The automatic network-state observation was removed, rather than expanded into connectivity diagnosis. The field now intentionally reports NOT_CHECKED.

Earlier local tests used psutil 7.2.2 in a source-run virtual environment. No raw private measurements, identifiers or answers are stored here. The prior screenshots describe the earlier build and do not verify the corrected wording.

## Windows corrected build — physical disconnected-network rerun pending

On a physically disconnected Windows device, rerun the interactive CLI and opt in to the four local observations. Confirm:

- The application runs offline.
- Basic network observation is NOT_CHECKED, with the intentional scope explanation.
- No connectivity probe occurs (also covered by code review and automated tests).
- Disk wording is Current drive root space.
- The plain support message has no method/timestamp metadata; the structured handoff retains provenance.
- No privilege/privacy/security prompts appear. If any appear, stop and review scope without bypassing them.

Record the result and updated public-safe screenshots. Automated tests blocking socket connection attempts do not establish physical disconnected-device verification. No connection or system configuration was changed automatically for this fix pass.

## macOS — CI compatibility evidence only

Windows and macOS CI pass on Python 3.10 and 3.13 for the preceding build; check the latest run for the corrected commit. CI is compatibility evidence only, not real-device support verification.

CI also runs on macOS, but no real macOS device verification has been completed, so macOS support is not currently claimed. A real macOS device is currently unavailable; verification remains pending.

When a real macOS device is available, record macOS and Python/psutil versions. Run as an ordinary user with fictional answers, try opting out and opting in to collection, and run the tests. Review both previews, GiB labels, current drive root wording, uptime, intentional network omission and privacy limitations. Test while disconnected; record unexpected output and public-safe screenshots. If any privilege/privacy/security prompt appears, STOP and review scope rather than bypassing it.

Neither Windows CI nor macOS CI substitutes for human device verification. No verified cross-platform support claim is made.
