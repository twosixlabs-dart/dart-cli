import click

from cli.global_options import dart_options, pass_dart_context
from ssh.ssh import open_ssh


@click.command(name='ssh')
@dart_options
@click.argument('node', required=True)
@pass_dart_context
def command(ctx, node):
    """Open a secure shell session with a DART node"""
    open_ssh(ctx, node)
