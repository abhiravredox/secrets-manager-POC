#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import CommandParser


def main():
    """Run administrative tasks."""

    parser = CommandParser()
    parser.add_argument("--env")
    try:
        env_option, rest = parser.parse_known_args(sys.argv)
        sys.argv = rest
        os.environ["env"] = env_option.env
    except:
        pass

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "secrets_manager_prototype.settings"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
