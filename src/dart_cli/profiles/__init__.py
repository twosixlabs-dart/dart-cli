import click
from dart_cli.cli.global_options import dart_options, pass_dart_context
from dart_cli.profiles import manage_profiles


@click.group(name='profiles')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for managing configuration profiles"""


command.add_command(manage_profiles.add_profile_command)
command.add_command(manage_profiles.remove_profile_command)
command.add_command(manage_profiles.ls_profiles_command)
command.add_command(manage_profiles.view_profile_command)
