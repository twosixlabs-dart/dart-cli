import click

from dart_cli.cli.global_options import dart_options, pass_dart_context


@click.group()
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for interacting with readers output"""