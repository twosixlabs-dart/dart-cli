
provision_targets = [
    'all',
    'pipeline',
    'core-pipeline',
    'batch',
]

deploy_targets = [
    'all',
    'pipeline',
    'core-pipeline',
    'batch',
    'batch-master',
    'batch-workers',
    'data',
    'data-master',
    'data-workers',
    'rest',
    'streaming',
    'analytics',
]

provision_to_deploy_targets_map = {
    'all': ['all'],
    'pipeline': ['pipeline'],
    'core-pipeline': ['core-pipeline'],
    'batch': ['batch'],
}
