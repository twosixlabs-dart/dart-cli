import click
from click import Context

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context
from pipeline.clean import clean_s3, get_opts, stop_containers_clear_data
from pipeline.deploy import deploy, get_deploy_targets_from_provision_targets
from pipeline.diab import deploy_diab, stop_diab
from pipeline.provision import provision, destroy, start_pipeline, stop_pipeline, info_pipeline


@click.command(name='provision')
@dart_options
@click.argument('targets', type=click.Choice(['all', 'pipeline', 'core-pipeline', 'batch'], case_sensitive=False), nargs=-1, required=True)
@pass_dart_context
def provision_command(dart_context, targets):
    """Provisioning DART infrastructure"""
    provision(dart_context, targets)

@click.command(name='deploy')
@dart_options
@click.option('--ec2-ini-path', default=None, help='Path to an ec2.ini configuration (TST deployment environment only)')
@click.option('--deploy-remote', flag_value=True, default=False, help='Deploy services on remote instance using ssh (Dart-in-a-Box deployment environment only)')
@click.argument('targets', type=click.Choice(['all', 'pipeline', 'core-pipeline', 'analytics', 'batch', 'batch-master', 'batch-workers', 'data', 'data-master', 'data-workers', 'rest', 'streaming'], case_sensitive=False), nargs=-1, required=False, default=None)
@pass_dart_context
def deploy_command(dart_context: DartContext, ec2_ini_path, deploy_remote, targets):
    """Deploy DART services"""
    if dart_context.dart_env.env_type() == 'default':
        choice = None
        while choice is None:
            y_or_n = input('This will deploy Dart-in-a-Box, erasing any saved data. Are you sure you want to proceed? (Y/n)')
            if y_or_n == 'Y':
                choice = True
            if y_or_n == 'n':
                choice = False
        if choice:
            deploy_diab(dart_context, deploy_remote)
        else:
            return
    elif dart_context.dart_env.env_type() == 'tst':
        if targets is None:
            targets = 'all'
        deploy(dart_context, ec2_ini_path, targets)
    else:
        raise click.ClickException('Deploy command unsupported for custom deployment environment')


@click.command(name='refresh')
@dart_options
@click.option('--vm-username', default='ubuntu', help='Username to login to the VM')
@click.option('--ec2-ini-path', default=None, help='Path to an ec2.ini configuration')
@click.option('--save-raws', is_flag=True, default=False, help='Preserves raws documents in s3')
@pass_dart_context
def refresh_command(dart_context: DartContext, vm_username, ec2_ini_path, save_raws):
    """Clear data and redeploy all DART services"""
    print(f'Warning! Running this command will delete all data in {dart_context.dart_env.env}')
    res = input('Do you wish to proceed (n/Y)   ')
    if res != 'Y':
        print('aborting...')
        exit(1)
    status = True
    if not save_raws:
        status = clean_s3(dart_context, get_opts(dart_context, True))
    if status:
        if stop_containers_clear_data(dart_context, vm_username, ec2_ini_path):
            if not deploy(dart_context, vm_username, ec2_ini_path, 'all'):
                print('Redeployment of services failed')
        else:
            print('Failed to stop services and/or clear data')
    else:
        print('Failed to clean s3 buckets (aborted)')

@click.command(name='provision-deploy')
@dart_options
@click.option('--vm-username', default='ubuntu', help='Username to login to the VM')
@click.option('--ec2-ini-path', default=None, help='Path to an ec2.ini configuration')
@click.argument('targets', type=click.Choice(['all', 'pipeline', 'core-pipeline', 'batch'], case_sensitive=False), nargs=-1, required=True)
@pass_dart_context
def provision_deploy_command(dart_context: DartContext, vm_username, ec2_ini_path, targets):
    """DART cli command for provisioning and deploying DART infrastructure"""
    if dart_context.dart_env.env_type() != 'tst':
        raise click.ClickException('Provision command supported only for TST deployment environment')

    provision_success = provision(dart_context, targets)
    if provision_success:
        deploy_targets = get_deploy_targets_from_provision_targets(targets)
        print(deploy_targets)
        deploy(dart_context, vm_username, ec2_ini_path, deploy_targets)
    else:
        print('Provision failed -- cancelling deployment')

@click.command(name='destroy')
@dart_options
@click.argument('targets', type=click.Choice(['all', 'pipeline', 'core-pipeline', 'batch'], case_sensitive=False), nargs=-1, required=True)
@pass_dart_context
def destroy_command(dart_context, targets):
    """DART cli command for provisioning DART infrastructure"""
    if dart_context.dart_env.env_type() != 'tst':
        raise click.ClickException('Destroy command supported only for TST deployment environment')

    print(f'Warning! Running this command will remove all service infrastructure in {dart_context.dart_env.env}')
    res = input('Do you wish to proceed (n/Y)   ')
    if res != 'Y':
        print('aborting...')
        exit(1)
    destroy(dart_context, targets)

@click.command(name='start')
@dart_options
@pass_dart_context
def start_command(dart_context : DartContext):
    """Start all stopped DART instances"""
    if dart_context.aws_profile is None:
        raise click.exceptions.MissingParameter( "missing aws profile: --aws-profile" )
    if dart_context.dart_env.env is None:
        raise click.exceptions.MissingParameter( "missing DART environment: --env/-e" )
    start_pipeline(dart_context)

@click.command(name='stop')
@dart_options
@pass_dart_context
def stop_command(dart_context: DartContext):
    """Stop all DART instances"""
    if dart_context.dart_env.env_type() == 'default':
        stop_diab()
    if dart_context.aws_profile is None:
        raise click.exceptions.MissingParameter( "missing aws profile: --aws-profile" )
    if dart_context.dart_env.env is None:
        raise click.exceptions.MissingParameter( "missing DART environment: --env/-e" )
    stop_pipeline(dart_context)

@click.command(name='info')
@dart_options
@pass_dart_context
def info_command(dart_context):
    """Stop all DART instances"""
    if dart_context.aws_profile is None:
        raise click.exceptions.MissingParameter( "missing aws profile: --aws-profile" )
    if dart_context.dart_env.env is None:
        raise click.exceptions.MissingParameter( "missing DART environment: --env/-e" )
    info_pipeline(dart_context)

@click.command(name='clean-s3')
@dart_options
@click.option('--no-prompt/--prompt', default=False)
@pass_dart_context
def clean_command(dart_context, no_prompt):
    """Empty all contents of an environment's s3 buckets"""
    if not no_prompt:
        print(f'Warning! Running this command will delete all stored raw documents and upload metadata in {dart_context.dart_env.env}')
        res = input('Do you wish to proceed (n/Y)   ')
        if res != 'Y':
            print('aborting...')
            exit(1)

    clean_s3(dart_context, get_opts(dart_context, no_prompt))

@click.command(name='nuke')
@dart_options
@pass_dart_context
@click.pass_context
def nuke_command(ctx: Context, dart_context: DartContext):
    """Destroy an existing DART environment"""
    ctx.invoke(clean_command, no_prompt=False)
    ctx.invoke(destroy_command, targets=['all'])
