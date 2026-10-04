"""Terminal preview only: no automatic save, clipboard action or sending."""
from .collectors import collect
from .questionnaire import ask
from .reports import render


def main():
    print("Before You Call IT — source-run prototype")
    print("On a company-managed device, ask your IT team before running unapproved software.")
    print("Do not enter passwords, authentication codes, API keys or other secrets.")
    print("Answers are optional. Review the preview carefully before sharing.")
    try:
        answers = ask()
        consent = input("Read five basic local observations? (OS, RAM capacity, system volume space, uptime, interface enabled; no internet request) [y/N] ")
        observations = collect() if consent.strip().lower() == "y" else []
        structured, plain = render(answers, observations)
        print("\n" + structured + "\n\n--- Plain support message ---\n\n" + plain)
    except (KeyboardInterrupt, EOFError):
        print("\nStopped. Nothing was sent or saved by this tool.")


if __name__ == "__main__":
    main()
