#!/usr/bin/env python
"""Build the ReportLab User Guide MkDocs site with i18n support."""

import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MKDOCS_YML = os.path.join(SCRIPT_DIR, 'mkdocs.yml')


def main():
    subprocess.run(
        [sys.executable, '-m', 'mkdocs', 'build', '-f', MKDOCS_YML, '--clean'],
        cwd=SCRIPT_DIR
    )
    print(f'Site built to: {os.path.join(SCRIPT_DIR, "site")}')


if __name__ == '__main__':
    main()
