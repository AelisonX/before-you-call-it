"""Fixed-order reports; measurements and limited interpretation stay separate."""
from .collectors import KEYS, NETWORK_REASON
from .model import State
from .privacy import redact
from .questionnaire import QUESTIONS

OMISSIONS = "Account permissions; VPN configuration; internal/company server status; hardware health; malware; security software; application licensing; organisational access controls; company security policy."
PRIVACY = "Generated locally; not automatically sent anywhere. Review before sharing. Error messages and other answers can contain private information. Automatic omissions are incomplete. Automatic observations do not collect usernames, hostnames, or network identifiers. Free-text answers may still contain identifying information. Review before sharing. Output remains in this terminal and its scrollback; no report file is saved."
LABELS = {"os": "Operating system", "ram": "Installed memory", "disk": "Current drive root space", "uptime": "Uptime", "network": "Basic network observation"}


def describe(obs):
    if obs.state != State.OBSERVED:
        explanation = obs.reason or "This item was not checked. You can skip it or provide information manually to support."
        return f"{obs.state.value}: {explanation} Missing information does not establish a device fault."
    if obs.key == "ram":
        return f"{obs.value / 2**30:.2f} GiB"
    if obs.key == "uptime":
        return f"{int(obs.value // 3600)} hours {int(obs.value % 3600 // 60)} minutes"
    return str(obs.value)


def observations_text(observations, include_provenance=True):
    lines = []
    for key in KEYS:
        if key == "network":
            lines.append(f"{LABELS[key]}: NOT_CHECKED. {NETWORK_REASON}")
            continue
        matches = [o for o in observations if o.key == key]
        if not matches:
            lines.append(f"{LABELS[key]}: NOT_CHECKED. You may provide this manually or skip it.")
        else:
            for obs in matches:
                text = f"{LABELS[key]}: {describe(obs)}"
                if include_provenance:
                    text += f" [method: {obs.method}; observed at: {obs.timestamp or 'not recorded'}]"
                lines.append(text)
            if len({(o.state, str(o.value)) for o in matches}) > 1:
                lines.append("Conflicting observations are shown above. Interpretation: UNKNOWN. This tool cannot determine the cause.")
    return "\n".join(lines)


def render(answers, observations):
    safe = {key: redact(answers.get(key, "")) or "Not provided" for key, _ in QUESTIONS}
    facts = observations_text(observations)
    plain_facts = observations_text(observations, include_provenance=False)
    direction = "Share these details with your authorised IT/support team. This tool cannot determine the cause."
    if safe["others"].lower() == "coworkers":
        direction = "You reported that coworkers are affected. This may be useful information for IT/support. This tool cannot determine the cause."
    structured = "Support Request\n\n" + "\n\n".join(prompt + "\n" + safe[key] for key, prompt in QUESTIONS)
    structured += f"\n\nBasic device information\n{facts}\n\nWhat this tool did not check\n{OMISSIONS}\n\nSuggested support direction\n{direction}\n\nPrivacy\n{PRIVACY}"
    plain = (f"Hi IT Support,\n\nI was trying to: {safe['task']}\nWhat happened: {safe['symptom']}\n"
             f"Error message: {safe['error']}\nWhen it started: {safe['started']}\nRecent changes: {safe['changes']}\n"
             f"Other people affected: {safe['others']}\nWhat I already tried: {safe['tried']}\n\n"
             f"Basic local observations:\n{plain_facts}\n\nWhat this tool did not check:\n{OMISSIONS}\n\n{direction}\n"
             f"Could you please let me know what information you need next?\n\nThanks.\n\nPrivacy\n{PRIVACY}")
    return structured, plain
