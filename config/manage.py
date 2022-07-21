#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
load_dotenv()
NAME = os.getenv('NAME')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          NAME + ".settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
