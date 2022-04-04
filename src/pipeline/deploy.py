import click

from dart_context.dart_context import DartContext
from pipeline.parameter_data import provision_to_deploy_targets_map
from utilities.docker_utils import run_dart_docker_command


def deploy_default(version: str) -> None:
    """Retrieve and stand up dart-in-a-box"""
    pass


def stop_default(version: str) -> None:
    """Stop a running dart-in-a-box deployment"""
    pass


def get_deploy_targets_from_provision_targets(targets):
    deploy_targets = set()
    provision_targets = set(targets)
    for target in provision_targets:
        deploy_targets = deploy_targets.union(provision_to_deploy_targets_map[target])
    return deploy_targets


def deploy(dart_context: DartContext, ec2_ini_path, targets):
    deploy_options = get_deploy_opts(dart_context, ec2_ini_path)
    unique_targets = set(targets)
    if 'core-pipeline' in unique_targets:
        unique_targets.discard('data')
        unique_targets.discard('data-master')
        unique_targets.discard('data-workers')
        unique_targets.discard('rest')
        unique_targets.discard('streaming')
    if 'pipeline' in unique_targets:
        unique_targets.discard('core-pipeline')
        unique_targets.discard('data')
        unique_targets.discard('data-master')
        unique_targets.discard('data-workers')
        unique_targets.discard('rest')
        unique_targets.discard('streaming')
    if 'data' in unique_targets:
        unique_targets.discard('data-master')
        unique_targets.discard('data-workers')
    if 'batch' in unique_targets:
        unique_targets.discard('batch-master')
        unique_targets.discard('batch-workers')
    if 'all' in unique_targets:
        return deploy_all(dart_context, deploy_options)
    else:
        return_status = True
        for target in unique_targets:
            if target == 'pipeline':
                if not deploy_pipeline(dart_context, deploy_options):
                    return_status = False
            if target == 'core-pipeline':
                if not deploy_core_pipeline(dart_context, deploy_options):
                    return_status = False
            if target == 'analytics':
                if not deploy_analytics(dart_context, deploy_options):
                    return_status = False
            if target == 'batch':
                if not deploy_batch(dart_context, deploy_options):
                    return_status = False
            if target == 'batch-master':
                if not deploy_batch_master(dart_context, deploy_options):
                    return_status = False
            if target == 'batch-workers':
                if not deploy_batch_workers(dart_context, deploy_options):
                    return_status = False
            if target == 'data':
                if not deploy_data(dart_context, deploy_options):
                    return_status = False
            if target == 'data-master':
                if not deploy_data_master(dart_context, deploy_options):
                    return_status = False
            if target == 'data-workers':
                if not deploy_data_workers(dart_context, deploy_options):
                    return_status = False
            if target == 'rest':
                if not deploy_rest(dart_context, deploy_options):
                    return_status = False
            if target == 'streaming':
                if not deploy_streaming(dart_context, deploy_options):
                    return_status = False

        return return_status


def get_deploy_opts(dart_context: DartContext, ec2_ini_path):
    vm_username = dart_context.dart_env.tst_env.ssh_user
    vm_username_opt = '' if vm_username is None else f' --vm_username {vm_username}'
    ec2_ini_path_opt = '' if ec2_ini_path is None else f' --ec2_ini_path {ec2_ini_path}'
    if dart_context.dart_env.env is None:
        raise Exception('missing DART environment: provide with --env or config profiles')
    if dart_context.docker_un is None:
        raise Exception('missing docker username: provide with --docker_commands-auth or config profiles')
    if dart_context.docker_pw is None:
        raise Exception('missing docker password: provide with --docker_commands-auth or config profiles')
    if dart_context.aws_profile is None:
        raise Exception('missing AWS profiles: provide with --aws-profiles or add to config')
    if dart_context.ssh_key is None:
        raise Exception('missing ssh key path : provide with --ssh-key or add to config')

    docker_registry_username_opt = f' --docker_registry_username {dart_context.docker_un}'
    docker_registry_password_opt = f' --docker_registry_password {dart_context.docker_pw}'
    aws_profile_opt = f' --aws_profile {dart_context.aws_profile}'
    ssh_key_path_opt = f' --ssh_key_path /root/.ssh/{dart_context.ssh_key}'
    deploy_env_opt = f' --deploy_env {dart_context.dart_env.env}'

    return vm_username_opt \
        + ec2_ini_path_opt \
        + docker_registry_password_opt \
        + docker_registry_username_opt \
        + aws_profile_opt \
        + ssh_key_path_opt \
        + deploy_env_opt


def deploy_all(dart_context, deploy_options):
    if deploy_pipeline(dart_context, deploy_options):
        return deploy_batch(dart_context, deploy_options)
    else:
        return False


def deploy_pipeline(dart_context, deploy_options):
    if not deploy_core_pipeline(dart_context, deploy_options):
        return False


def deploy_core_pipeline(dart_context, deploy_options):
    base_command = './start-dart-distributed.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_analytics(dart_context, deploy_options):
    base_command = './start-analytics.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_batch(dart_context, deploy_options):
    base_command = './start-batch.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)

def deploy_batch_master(dart_context, deploy_options):
    base_command = './start-batch-master.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_batch_workers(dart_context, deploy_options):
    base_command = './start-batch-workers.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_data(dart_context, deploy_options):
    if deploy_data_master(dart_context, deploy_options):
        return deploy_data_workers(dart_context, deploy_options)
    else:
        return False


def deploy_data_master(dart_context, deploy_options):
    base_command = './start-data-master.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_data_workers(dart_context, deploy_options):
    base_command = './start-data-workers.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_rest(dart_context, deploy_options):
    base_command = './start-rest.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_streaming(dart_context, deploy_options):
    base_command = './start-streaming.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)
