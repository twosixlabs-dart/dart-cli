from typing import Callable

from dart_context.dart_config import DartConfig
from dart_context.dart_environment.dart_environment_type import DartEnvironmentType


class DefaultDartEnvironmentType(DartEnvironmentType):
    """
    Deployment configuration for dart-in-a-box. Can be configured for local
    or remote deployment
    """

    host: str = None
    user: str = None
    data_dir: str = None
    version: str = None

    def set_host(self, new_host) -> None:
        self.host = new_host

    def set_user(self, new_user) -> None:
        self.user = new_user

    def set_data_dir(self, new_data_dir) -> None:
        self.data_dir = new_data_dir

    def set_version(self, new_version) -> None:
        self.version = new_version

    __service_map = {
        'corpex': {
            'port': 8088,
        },
        'forklift': {
            'port': 8091,
        },
        'cdr-retrieval': {
            'port': 8090,
            'base_name': 'cdrs',
            'container': 'cdr-retrieval',
        },
        'readers-output': {
            'port': 13337,
            'base_name': 'readers',
            'container': 'reader-output',
        },
        'tenants': {
            'port': 8080,
            'container': 'dart-tenants',
        },
        # 'reprocess': {
        #     'port': 6309,
        #     'container': 'daydream-nation',
        # },
        # 'users': {
        #     'port': ,
        #     'container': 'dart-users',
        # },
        'dart': {
            'container': 'dart-3',
        },
        'postgres': {
            'port': 5432,
            'container': 'dart-postgres',
        },
        'elasticsearch': {
            'port': 9200,
            'container': 'dart-es',
        },
        'arango': {
            'port': 8529,
            'container': 'dart-arangodb',
        },
    }

    def service_instance(self, service: str) -> str:
        if self.host is None:
            return 'local'
        return 'remote'

    def instance_host(self, instance: str) -> str:
        if self.host is None:
            return 'localhost'
        return self.host

    def service_port(self, service: str, direct: bool = False) -> int:
        return self.__service_map[service]['port']

    def service_base_path(self, service: str, direct: bool = False) -> str:
        base_name = service if 'base_path' not in self.__service_map[service] else self.__service_map[service]['base_name']
        return f'/dart/api/v1/{base_name}'

    def service_container_name(self, service: str) -> str:
        return service if 'container' not in self.__service_map[service] else self.__service_map[service]['container']

    def service_base_url(self, service: str, direct: bool = False) -> str:
        host = self.host if self.host is not None else 'localhost'
        return f'http://{host}:{self.service_port(service, direct)}{self.service_base_path(service, direct)}'

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'host': (lambda: self.host, lambda h: self.set_host(h)),
            'user': (lambda: self.user, lambda u: self.set_user(u)),
            'data-dir': (lambda: self.data_dir, lambda dd: self.set_data_dir(dd)),
            'version': (lambda : self.version, lambda v: self.set_version(v)),
        }
