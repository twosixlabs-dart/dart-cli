import json

from setuptools import setup, find_packages

setup_data_file = open('setup_data.json', 'rt')
setup_data = json.loads(setup_data_file.read())
setup_data_file.close()

tests_require = [
    'pytest',
    'mock',
    'moto',
]

install_requires = [
    'click',
    'pytest',
    'boto3',
    'botocore',
    'requests',
    'docker',
    'dockerpty',
    'pyjwt',
    'kafka-python',
]

setup(
    name=setup_data['name'],
    version=setup_data['version'],
    description='Command line interface with DART services',
    author='John Hungerford',
    author_email='john.hungerford@twosixlabs.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    py_modules=['dart', 'common_options', 'dart_context'],
    entry_points=f'''
        [console_scripts]
        {setup_data['cmd']}=cli.dart:cli
    ''',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    include_package_data=True,
)
