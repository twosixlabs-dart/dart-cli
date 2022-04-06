import os

from dart_context.dart_context import DartContext


def compose_file_url(context: DartContext) -> str:
    version = context.dart_env.default_env.version
    if version is None:
        branch_segment = 'master'
    elif len(version.split('.')) == 3:
        branch_segment = f'v{version.strip().lstrip("v")}'
    else:
        branch_segment = version.strip()

    return f'https://raw.githubusercontent.com/twosixlabs-dart/dart-in-the-box/{branch_segment}/dart-standalone.yml'


def clean_command(data_root: str, user: str):
    data_dir = f'{data_root}/data'
    es_dirs = f'{data_dir}/dart-es-master {data_dir}/dart-es-replica-1 {data_dir}/dart-es-replica-2'
    return f'rm -rf {data_dir}; mkdir -p {es_dirs}; chown -R {user}: {data_dir}'


def command_with_docker_compose(context: DartContext, cmd: str) -> str:
    data_root = context.dart_env.default_env.data_dir if context.dart_env.default_env.data_dir is not None else '.'
    return f'cd {data_root}; rm -f docker-compose.yml; curl {compose_file_url(context)} --output docker-compose.yml; {cmd}; rm -f docker-compose.yml'


def deploy_diab(context: DartContext, remote: bool, version: str = 'latest') -> None:
    clean_diab(context, remote)
    start_diab(context, remote)


def start_diab(context: DartContext, remote: bool) -> None:
    start_cmd = 'docker-compose up -d'
    full_cmd = command_with_docker_compose(context, start_cmd)
    execute(context, full_cmd, remote)


def stop_diab(context: DartContext, remote: bool, version: str = 'latest') -> None:
    stop_cmd = 'docker-compose down'
    full_cmd = command_with_docker_compose(context, stop_cmd)
    execute(context, full_cmd, remote)


def clean_diab(context: DartContext, remote: bool) -> None:
    data_root = context.dart_env.default_env.data_dir if context.dart_env.default_env.data_dir is not None else '.'
    user = context.dart_env.default_env.user if context.dart_env.default_env.data_dir is not None else '$USER'
    cmd = clean_command(data_root, user)
    execute(context, cmd, remote)


def execute(dart_context: DartContext, cmd: str, remote: bool) -> None:
    if not remote:
        command = cmd
    else:
        host = dart_context.dart_env.default_env.host
        id_opt = f'-i ~/.ssh/{dart_context.ssh_key}' if dart_context.ssh_key is not None else ''
        user = dart_context.dart_env.default_env.user if dart_context.dart_env.default_env.user is not None else 'ubuntu'
        command = f'ssh {id_opt} -t {user}@{host} \'{cmd}\''

    print(command)
    os.system(command)
