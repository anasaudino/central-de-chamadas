from django.core.management import execute_from_command_line
import os
import sys


def main() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
