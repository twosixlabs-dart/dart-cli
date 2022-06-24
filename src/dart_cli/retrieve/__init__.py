import click

from dart_cli.cli.global_options import dart_options, pass_dart_context
from dart_cli.retrieve.cdr_archive import get_cdr_archive
from dart_cli.retrieve.cdr_retrieval import get_cdrs, get_raws


@click.group(name='retrieve')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for retrieving DART artifacts"""


command.add_command(get_cdr_archive)
command.add_command(get_cdrs)
command.add_command(get_raws)
