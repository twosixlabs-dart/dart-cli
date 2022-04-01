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
@click.argument('post-fix', required=False, default='')
def update_version(post_fix: str):
    """Update setup.py version from app.version"""
    with open(app_version_path, 'r') as app_version_file:
        app_version = app_version_file.read().strip()
        with open(setup_path, 'r+t') as setup_file:
            setup_data = json.loads(setup_file.read())
            setup_version = setup_data['version']
            if app_version == 'latest':
                new_setup_version = setup_version + post_fix
            else:
                new_setup_version = app_version + post_fix
            setup_data['version'] = new_setup_version
            setup_file.seek(0)
            setup_file.write(json.dumps(setup_data, indent=4))
            setup_file.truncate()


@click.group()
def cli():
    """Manage versions for publication"""


cli.add_command(update_version)

cli()
