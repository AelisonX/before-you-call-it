"""Fixture, failure, uncertainty, privacy and offline tests."""
import ast
from contextlib import ExitStack
from pathlib import Path
import socket
import unittest
from unittest.mock import patch
import psutil
from before_you_call_it.model import Observation, State
from before_you_call_it.collectors import collect
from before_you_call_it.questionnaire import ask, QUESTIONS
from before_you_call_it.reports import render, describe
from before_you_call_it.privacy import redact


class PrototypeTests(unittest.TestCase):
    def test_states(self):
        for state in (State.UNAVAILABLE, State.NOT_CHECKED):
            self.assertRaises(ValueError, Observation, 'ram', 0, state=state)
        self.assertRaises(ValueError, Observation, 'ram', state=State.OBSERVED)

    def test_units(self):
        self.assertEqual(describe(Observation('ram', 2**30, state=State.OBSERVED)), '1.00 GiB')
        self.assertEqual(describe(Observation('uptime', 3661, state=State.OBSERVED)), '1 hours 1 minutes')

    def test_missing(self):
        for report in render({}, []):
            for text in ('NOT_CHECKED', 'What this tool did not check', 'Review before sharing'):
                self.assertIn(text, report)
            self.assertNotIn('0.00 GiB', report)

    def test_failures(self):
        targets = ('platform.system', 'psutil.virtual_memory', 'psutil.disk_usage', 'psutil.boot_time')
        with ExitStack() as stack:
            for target in targets:
                stack.enter_context(patch('before_you_call_it.collectors.' + target, side_effect=OSError('PRIVATE')))
            observations = collect()
        self.assertTrue(all(o.state == State.UNAVAILABLE and o.value is None for o in observations if o.key != "network"))
        self.assertEqual(observations[-1].state, State.NOT_CHECKED)
        for report in render({}, observations):
            self.assertNotIn('PRIVATE', report)
            self.assertIn('skip', report)

    def test_access_denied(self):
        with patch('before_you_call_it.collectors.psutil.virtual_memory', side_effect=psutil.AccessDenied()):
            obs = next(o for o in collect() if o.key == 'ram')
        self.assertEqual(obs.state, State.UNAVAILABLE)
        self.assertIsNone(obs.value)

    def test_conflict(self):
        fixture = [Observation('ram', value, state=State.OBSERVED) for value in (2**30, 2**31)]
        for report in render({}, fixture):
            for text in ('Conflicting observations', 'UNKNOWN', '1.00 GiB', '2.00 GiB'):
                self.assertIn(text, report)

    def test_network_intentionally_not_checked(self):
        obs = next(o for o in collect() if o.key == "network")
        self.assertEqual(obs.state, State.NOT_CHECKED)
        self.assertIsNone(obs.value)
        self.assertEqual(obs.timestamp, "")
        for report in render({}, collect()):
            self.assertIn("Basic network observation: NOT_CHECKED.", report)
            self.assertIn("does not perform connectivity probes or inspect network identifiers", report)

    def test_questions(self):
        answers = ask(lambda prompt: ' example ')
        self.assertEqual(len(answers), 7)
        self.assertTrue(all(value == 'example' for value in answers.values()))

    def test_privacy(self):
        text = r'user@example.test https://internal.test 192.168.1.1 aa:bb:cc:dd:ee:ff C:\Users\PRIVATE\file username=PRIVATE hostname=HOST ssid=WIFI token=SECRET'
        for report in render({key: text for key, _ in QUESTIONS}, []):
            for private in ('user@example.test', 'internal.test', '192.168.1.1', 'aa:bb:cc:dd:ee:ff', 'PRIVATE', 'HOST', 'WIFI', 'SECRET'):
                self.assertNotIn(private, report)

    def test_network_apis_not_called(self):
        with patch.object(psutil, "net_if_stats", side_effect=AssertionError("Network API")), patch.object(psutil, "net_if_addrs", side_effect=AssertionError("Identifiers")):
            collect()

    def test_current_drive_root_wording(self):
        observations = collect()
        disk = next(o for o in observations if o.key == "disk")
        self.assertIn("current drive root", disk.method)
        for report in render({}, observations):
            self.assertIn("Current drive root space", report)
            self.assertNotIn("System volume", report)

    def test_time_preserved(self):
        self.assertEqual(redact("Started at 14:30:05"), "Started at 14:30:05")

    def test_ipv6_omitted(self):
        for address in ("fe80::1", "2001:db8::1", "::1", "2001:db8:0:0:0:0:0:1"):
            self.assertEqual(redact(address), "[omitted]")

    def test_plain_without_provenance(self):
        fixture = [Observation("ram", 2**30, method="fixture", timestamp="fixture-time", state=State.OBSERVED)]
        structured, plain = render({}, fixture)
        for label in ("method:", "observed at:"):
            self.assertIn(label, structured)
            self.assertNotIn(label, plain)
        self.assertIn("1.00 GiB", plain)
        self.assertIn("What this tool did not check", plain)
        self.assertIn("Automatic omissions are incomplete", plain)

    def test_deterministic(self):
        fixture = [Observation('ram', 2**30, timestamp='fixture', state=State.OBSERVED)]
        self.assertEqual(render({}, fixture), render({}, fixture))

    def test_coworker_rule(self):
        self.assertIn('You reported that coworkers', render({'others': 'coworkers'}, [])[0])
        self.assertNotIn('You reported that coworkers', render({'others': 'only me'}, [])[0])

    def test_language(self):
        text = '\n'.join(render({}, collect())).lower()
        for word in ('healthy', 'no problems', 'damaged', 'infected', 'virus', 'danger', 'critical', 'fixed'):
            self.assertNotIn(word, text)

    def test_no_network_connection_attempt(self):
        with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network request')):
            self.assertEqual(len(collect()), 5)
            render({}, collect())

    def test_static_scope(self):
        allowed = {'os', 'platform', 'time', 'datetime', 'psutil', 'dataclasses', 'enum', 're', 'ipaddress'}
        for path in Path('before_you_call_it').glob('*.py'):
            source = path.read_text(encoding='utf-8-sig')
            for node in ast.walk(ast.parse(source)):
                if isinstance(node, ast.Import):
                    self.assertTrue(all(a.name in allowed for a in node.names))
                if isinstance(node, ast.ImportFrom) and node.level == 0:
                    self.assertIn(node.module, allowed)
                if isinstance(node, ast.keyword) and node.arg == 'shell':
                    self.fail('Shell execution is outside scope')
            for forbidden in ('sudo', 'runas', 'process_iter', 'net_if_stats', 'net_if_addrs', 'environ', 'gethostname', 'getuser'):
                self.assertNotIn(forbidden, source)


if __name__ == '__main__':
    unittest.main()
