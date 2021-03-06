import click

from dart_cli.dart_context.dart_context import DartContext

from dart_cli import health, users, local, auth, profiles, ssh, messages, retrieve, tenants, pipeline, reprocess, \
    corpex, forklift
from dart_cli.cli.global_options import dart_options, pass_dart_context

from importlib.metadata import version

from dart_cli.docker_commands import psql_command, debug_command, logs_command


@click.group()
@dart_options
@click.version_option(version('dart-cli'))
@pass_dart_context
def cli(ctx: DartContext):
    """Root command for DART command line interface."""


cli.add_command(profiles.command)
cli.add_command(retrieve.command)
cli.add_command(corpex.command)
cli.add_command(local.command)
cli.add_command(forklift.command)
cli.add_command(reprocess.command)
cli.add_command(ssh.command)
cli.add_command(psql_command)
cli.add_command(debug_command)
cli.add_command(logs_command)
cli.add_command(messages.command)
cli.add_command(pipeline.command)
cli.add_command(health.command)
cli.add_command(auth.command)
cli.add_command(tenants.command)
cli.add_command(users.command)
