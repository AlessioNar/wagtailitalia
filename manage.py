#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
load_dotenv()
PROJECT_NAME = os.getenv('PROJECT_NAME')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          PROJECT_NAME + ".settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
