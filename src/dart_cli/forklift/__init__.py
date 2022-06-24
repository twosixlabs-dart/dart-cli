import click

from dart_cli.cli import global_options
from dart_cli.forklift.submit import submit_command


@click.group(name='forklift')
@global_options.dart_options
@global_options.pass_dart_context
def command(dart_context):
    """Commands for submitting raw documents to DART"""


command.add_command(submit_command)
