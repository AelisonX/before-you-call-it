# Real-device verification

Date: 2026-10-04 (Australia/Brisbane).

Public position: **Tested on Windows 11.** Distribution remains a Windows-tested source-run prototype, with no packaged executable or unsigned executable distribution. The corrected Windows build physical disconnected-network rerun is COMPLETE/PASS, as reported by the project owner. The required Windows verification is complete for publication as a Windows-tested source-run prototype.

## Windows PC — earlier publication evidence

The project owner reported completion on Windows 11 (previously recorded OS build: 10.0.26200):

- Interactive CLI flow completed; the original five collectors were exercised.
- No UAC, privacy, Defender or SmartScreen prompts appeared.
- An actual disconnected-network run completed successfully.
- Public-safe screenshots were captured; files are not included in this repository.

The earlier physical disconnected-network run produced “A network interface appears available.” Post-build review found this could be satisfied by loopback or virtual interfaces, so it was not useful enough to retain. The automatic network-state observation was removed, rather than expanded into connectivity diagnosis. The field now intentionally reports NOT_CHECKED.

Earlier local tests used psutil 7.2.2 in a source-run virtual environment. No raw private measurements, identifiers or answers are stored here. The prior screenshots describe the earlier build and do not verify the corrected wording.

## Windows corrected build — physical disconnected-network rerun COMPLETE/PASS

On 2026-10-04, the project owner reported these results on a real Windows 11 device, physically disconnected from the internet:

- The application ran successfully offline.
- The user opted in to the four local observations.
- Operating system, installed memory, current drive root space and uptime were collected successfully.
- Basic network observation displayed exactly: `NOT_CHECKED. This prototype does not perform connectivity probes or inspect network identifiers.`
- The structured handoff retained method/timestamp provenance.
- The plain support message did not include method/timestamp metadata.
- No UAC / Administrator, Windows privacy, Defender, SmartScreen or other privilege/security prompt appeared.

This is a completed physical disconnected-device test, separate from automated tests that block socket connection attempts. Code review and automated tests provide evidence that no connectivity probe occurs. Updated screenshots from this rerun have not been supplied or included in the repository; the earlier screenshot record remains unchanged.

## macOS — CI compatibility evidence only

The corrected implementation commit `42174d8` passed Windows and macOS CI on Python 3.10 and 3.13. CI is compatibility evidence only, not real-device support verification.

CI also runs on macOS, but no real macOS device verification has been completed, so macOS support is not currently claimed. A real macOS device is currently unavailable; verification remains pending.

When a real macOS device is available, record macOS and Python/psutil versions. Run as an ordinary user with fictional answers, try opting out and opting in to collection, and run the tests. Review both previews, GiB labels, current drive root wording, uptime, intentional network omission and privacy limitations. Test while disconnected; record unexpected output and public-safe screenshots. If any privilege/privacy/security prompt appears, STOP and review scope rather than bypassing it.

Neither Windows CI nor macOS CI substitutes for human device verification. No verified cross-platform support claim is made.
