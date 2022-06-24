import click

from dart_cli.cli.global_options import pass_dart_context, dart_options
from dart_cli.corpex import shave
from dart_cli.corpex import search, aggregate


@click.group(name='corpex')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for searching the DART collection"""

command.add_command(search.search_command)
command.add_command(search.count_command)
command.add_command(shave.command)
command.add_command(aggregate.aggregate_command)
