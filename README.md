# Before You Call IT

Turn “my computer isn’t working” into a support request someone can actually act on.

## Status

Revised V0.1: free, Windows-tested source-run prototype, not currently intended for sale. Tested on Windows 11. This is a support communication helper, not a diagnostic or repair product. It is not enterprise-ready.

CI also runs on macOS, but no real macOS device verification has been completed, so macOS support is not currently claimed.

If this is a company-managed device, ask your organisation’s IT team before installing or running unapproved software.

## What it does

Seven optional questions record your task, symptom, error, start time, recent changes, other people affected and actions already tried. With your confirmation it reads four local observations: OS/version, RAM capacity, current drive root total/free space and uptime. The network report field is intentionally NOT_CHECKED: this prototype does not perform connectivity probes or inspect network identifiers. It previews a structured Support Handoff and a plain-language IT message in your terminal. Copy only what you have reviewed.

OBSERVED means a value was read. UNAVAILABLE means the API could not read it; a safe explanation suggests skipping or providing information manually. NOT_CHECKED means no check was performed. None of these states is a diagnosis. Conflicts remain visible with UNKNOWN interpretation. RAM is capacity in GiB (2^30 bytes), not a utilisation score. Disk data covers the current drive root context, not a verified operating-system system volume. Network state is intentionally not checked.

## What it does not do

No administrator/root access, privilege escalation, shell execution, process lists, application/service discovery, network identifiers, connectivity probes, telemetry, analytics, LLM/cloud calls, persistent monitoring, health scores or automatic remediation. No account, VPN, hardware-health, malware, security-policy or licensing diagnosis. No automatic sending or clipboard operation.

## Run and develop

Python 3.10+ and psutil 7.x are required. psutil is the only runtime dependency; it provides shared OS APIs without parsing localised shell output. Installation needs internet to obtain dependencies; running the installed application does not.

```text
python -m venv .venv
```

Windows:

```text
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m before_you_call_it.cli
.venv\Scripts\python -m unittest discover -s tests -v
```

macOS development/verification commands only (not a claim of macOS support):

```text
.venv/bin/python -m pip install -e .
.venv/bin/python -m before_you_call_it.cli
.venv/bin/python -m unittest discover -s tests -v
```

Use ordinary user permissions. Do not bypass security warnings or grant additional access to get observations. If an unexpected privacy or privilege prompt appears, stop and review the collector's scope. Distribution remains a Windows-tested source-run prototype. No packaged Windows release or unsigned executable distribution is provided.

## Privacy and persistence

Automatic observations do not include usernames, hostnames, IP/MAC addresses, SSIDs, serial numbers, file paths, browser data, credentials or environment variables. No network interface APIs are called. Free-text answers may still contain identifying information. The disk path is used locally and never output. No data leaves the device during application execution.

Free-text answers can still contain sensitive data. Basic pattern-based omissions cover emails, URLs, common addresses/paths and labelled secrets or identifiers. This is deliberately incomplete: unlabelled names, server names, unusual paths or secrets can remain. Never enter passwords, authentication codes or keys. Review both previews before sharing. The application holds answers in memory, writes to terminal output/scrollback, and does not save report files. Terminal logging or the place you paste a report can retain it independently.

## Threat model

Minimal dependencies reduce, but do not eliminate, supply-chain risk. Review code and dependency updates. Reports can be pasted to the wrong recipient; minimise answers and review first. This tool must not use alarming claims to pressure users into payments, credential sharing or installation. It gives no potentially destructive troubleshooting advice. It does not protect against malware, compromised endpoints/accounts or malicious administrators.

## Testing and platform evidence

Tested on Windows 11. The completed real-device evidence includes the interactive CLI flow, the original five collectors, no unexpected privilege/privacy/security prompts, an actual disconnected-network run and public-safe screenshots. Post-build review removed the automatic network-state inference; the corrected build has completed its physical disconnected-network rerun on Windows 11 (COMPLETE/PASS), including all four local observations and both report formats. This evidence was reported by the project owner.

CI runs the same fixture and scope tests on Windows and macOS with Python 3.10 and 3.13. Both platforms pass CI; this is compatibility evidence only, not real-device support verification. CI also runs on macOS, but no real macOS device verification has been completed, so macOS support is not currently claimed. See [device verification](docs/device-verification.md) for the evidence record and pending Mac verification.

Tests cover state invariants, missing data, API failures, unit conversion, conflicts, intentional network omission, coworker wording, questionnaire input, privacy omissions, language safety, offline operation and static scope restrictions.

## Understandable file map

- `model.py`: explicit observation values, provenance and three states.
- `questionnaire.py`: seven human questions.
- `collectors.py`: four read-only API checks and an intentional network omission; no interpretation.
- `privacy.py`: conservative text omissions.
- `reports.py`: fixed-order formatting and a limited coworker rule, without cause inference.
- `cli.py`: questionnaire, optional collection and terminal preview.
- `tests/test_prototype.py`: known-input, failure, privacy and scope checks.
- `.github/workflows/tests.yml`: Windows/macOS test matrix.

## Example and limitations

See the [fictional Support Handoff](docs/example-handoff.txt). Every output visibly states what was not checked and asks for human support. The interface is English and terminal-based. No GUI, installer, cloud service, database or background service exists. Reports are snapshot observations, not proof of device health. Basic redaction is not complete; free-text input needs review.

## AI-assisted development and human role

The implementation and initial tests were generated with AI assistance. The project owner identified the workflow problem, directed and reduced scope, chose privacy boundaries and owns review and verification. This demonstrates scoped prototyping and support communication, not qualifications as a systems engineer, IT administrator or cybersecurity specialist. Before presenting it as portfolio-ready, the owner should be able to explain each file, collected/omitted data, failure states, report generation, sharing behavior and why elevated access is unnecessary.
