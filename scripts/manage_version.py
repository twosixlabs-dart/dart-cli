#!/usr/bin/env python3
import json
import os
from pathlib import Path
import click

sbt_name = 'version.sbt'
this_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = Path(this_dir).parent
sbt_path = project_dir.joinpath(sbt_name)

setup_name = 'setup_data.json'
setup_path = project_dir.joinpath(setup_name)

def parse_version(sbt_string: str):
    # version.sbt format is: 'version in ThisBuild := "1.0-SNAPSHOT"'
    [_, raw_version] = sbt_string.split(':=')
    return raw_version.strip('" ')

def gen_version(setup_version: str):
    if len(setup_version.split('.')) >= 3:
        return f'version in ThisBuild := "{gen_latest(setup_version)}"'

    return f'version in ThisBuild := "{setup_version}"'

def gen_latest(setup_version: str):
    split_version = setup_version.split('.')
    return '.'.join(split_version[:2]) + '-SNAPSHOT'

@click.command(name='from-sbt')
def from_sbt():
    """Populate setup.py version with version from version.sbt"""
    with open(sbt_path, 'rt') as sbt_file:
        sbt_string = sbt_file.read()
        sbt_version = parse_version(sbt_string)
        with open(setup_path, 'r+t') as setup_file:
            setup_data = json.loads(setup_file.read())
            setup_data['version'] = sbt_version
            setup_file.seek(0)
            setup_file.write(json.dumps(setup_data, indent=4))
            setup_file.truncate()


@click.command(name='to-sbt')
def to_sbt():
    """Populate version.sbt with setup.py version"""
    with open(setup_path, 'rt') as setup_file:
        setup_data = json.loads(setup_file.read())
        setup_version = setup_data['version']
        with open(sbt_path, 'wt') as sbt_file:
            sbt_file.write(gen_version(setup_version))

@click.command(name='set-latest')
def set_latest():
    """Make setup.py version X.X-SNAPSHOT"""
    with open(setup_path, 'r+t') as setup_file:
        setup_data = json.loads(setup_file.read())
        setup_version = setup_data['version']
        setup_data['version'] = gen_latest(setup_version)
        setup_file.seek(0)
        setup_file.write(json.dumps(setup_data, indent=4))
        setup_file.truncate()

@click.command(name='set-version')
@click.argument('version', required=True)
def set_version(version):
    """Update setup.py version"""
    with open(setup_path, 'r+t') as setup_file:
        setup_data = json.loads(setup_file.read())
        setup_data['version'] = version
        setup_file.seek(0)
        setup_file.write(json.dumps(setup_data, indent=4))
        setup_file.truncate()

@click.group()
def cli():
    """Move version from setup.py to version.sbt and vice versa"""

cli.add_command(from_sbt)
cli.add_command(to_sbt)
cli.add_command(set_latest)
cli.add_command(set_version)

cli()
