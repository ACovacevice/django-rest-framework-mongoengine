#!/usr/bin/env python
import os, sys

DEFAULT_SETTINGS_MODULE = "server.settings"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)

    import django
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
