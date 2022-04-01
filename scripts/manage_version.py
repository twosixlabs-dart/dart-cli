#!/usr/bin/env python3
import json
import os
from pathlib import Path
import click

this_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = Path(this_dir).parent

app_version_name = 'app.version'
app_version_path = project_dir.joinpath(app_version_name)

setup_name = 'setup_data.json'
setup_path = project_dir.joinpath(setup_name)


@click.command(name='update-version')
def update_version():
    """Update setup.py version from app.version"""
    with open(app_version_path, 'r') as app_version_file:
        app_version = app_version_file.read().strip()
        # Leave the setup version alone if latest
        if app_version == 'latest':
            return

        with open(setup_path, 'r+t') as setup_file:
            setup_data = json.loads(setup_file.read())
            setup_data['version'] = app_version
            setup_file.seek(0)
            setup_file.write(json.dumps(setup_data, indent=4))
            setup_file.truncate()


@click.group()
def cli():
    """Manage versions for publication"""


cli.add_command(update_version)

cli()
