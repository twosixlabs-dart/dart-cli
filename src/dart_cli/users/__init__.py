import click

from dart_cli.cli.global_options import pass_dart_context, dart_options
from dart_cli.users import ls_users, groups
from dart_cli.users import add_user, remove_users


@click.group(name='users')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for managing DART users"""

command.add_command(ls_users.ls_command)
command.add_command(ls_users.view_command)
command.add_command(add_user.add_command)
command.add_command(add_user.update_command)
command.add_command(groups.join_command)
command.add_command(remove_users.command)
