import click

from dart_cli.cli import global_options
from dart_cli.messages.read import read_command


@click.group(name='messages')
@global_options.dart_options
@global_options.pass_dart_context
def command(dart_context):
    """Commands for interacting with DART messaging"""


command.add_command(read_command)
