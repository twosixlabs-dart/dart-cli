import click
from dart_cli.local.filter import raw_filter, cdr_filter
from dart_cli.local.list import list_ids
from dart_cli.local.post import post_command
from dart_cli.local.hash import hash_files


@click.group(name='local')
def command():
    """Utilities for dealing with DART data locally"""


command.add_command(raw_filter)
command.add_command(cdr_filter)
command.add_command(post_command)
command.add_command(list_ids)
command.add_command(hash_files)
