import click

from dart_cli.auth import retrieve_token
from dart_cli.dart_context.dart_context import DartContext

from dart_cli.cli.global_options import dart_options, pass_dart_context


@click.group(name='auth')
@dart_options
@pass_dart_context
def command(context : DartContext):
    """Commands for managing DART authentication/authorization"""

command.add_command(retrieve_token.command)
