import click

from dart_cli.cli.global_options import pass_dart_context, dart_options
from dart_cli.tenants import add_tenants
from dart_cli.tenants import remove_tenants, tenant_docs, ls_tenants


@click.group(name='tenants')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for managing DART tenants"""

command.add_command(add_tenants.add_command)
command.add_command(add_tenants.clone_command)
command.add_command(tenant_docs.command)
command.add_command(ls_tenants.command)
command.add_command(remove_tenants.command)
