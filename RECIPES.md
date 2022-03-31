# DART CLI Recipes

This document provides the syntax for performing common DART tasks using the command line.

## Debugging

The cli includes some root-level commands for accessing instances and docker services.

### SSH (TST only)

The `ssh` command provides a shortcut for opening a secure shell connection to an instance:

```shell
$ dart --ssh-key [KEY] -e [ENV_NAME] ssh [INSTANCE_NAME]
```
e.g.,
```shell
$ dart -p prod -e wm ssh data-master
```

### docker-debug

To connect directly to a container running on an instance, you can use the `debug` command,
which runs `docker exec -it` on an ssh connection:

```shell
$ dart --ssh-key [KEY] -e [ENV_NAME] debug [SERVICE]
```
e.g.,
```shell
$ dart -p prod -e wm debug corpex
```

To see which services are supported, look in at `services.py` in the `data` package in this
repository. The dict exported in that module maps instances and container names to each 
service. To connect to a container not included in the `services` module, just use the 
container name instead of the service name, and set the instance with `--instance` or `-i`.

For instance, you can exec into the zookeeper containers on either the streaming node or
the data node by doing the following:

```shell
$ dart -p prod -e wm debug zookeeper-1 -i data-master
```
or
```shell
$ dart -p prod -e wm debug zookeeper-1 -i streaming
```

### docker logs

You can get the docker logs of an instance using:

```shell
$ dart --ssh-key [KEY] -e [ENV_NAME] debug [SERVICE] [-f]
```

You can manually set the instance and container name in the same manner as the `debug`
command. To maintain a connection and follow the logs in real time, you can set the 
`--follow` or `-f` flag:

```shell
$ dart -p prod -e wm logs -f corpex
```
```shell
$ dart -p prod -e wm logs -f -i streaming zookeeper-1
```

### psql

You can access an environment's postgres database as follows:

```shell
$ dart -p prod -e wm psql
```

This will connect you to the `dart_db` database as a root user.

## Uploading

### Basic usage

To upload individual files:

```shell
$ dart -p prod -e wm \
       forklift submit \
          --tenant "tenant1" \
          --tenant "tenant2" \
          --label "label 1" \
          --label "label 2" \
          /path/to/file1 \
          /path/to/file2
```

To upload a directory and failed uploads to a separate directory:

```shell
$ dart -p prod -e wm \
       forklift submit \
          --tenant "tenant1" \
          --tenant "tenant2" \
          --label "label 1" \
          --label "label 2" \
          --input-dir /path/to/input-dir
          -f /path/to/failed-dir # or --failed-dir
```

You can then try to upload the failed documents again, moved success back to the original
directory:

```shell
$ dart -p prod -e wm \
       forklift submit \
          --tenant "tenant1" \
          --tenant "tenant2" \
          --label "label 1" \
          --label "label 2" \
          --input-dir /path/to/failed-dir2
          -s /path/to/input-dir # or --succeeded-dir
```

### Metadata

To set the metadata for the uploads using a json string:

```shell
$ dart -p prod -e wm \
       forklift submit \
          --metadata '{"tenants":["tenant-1","tenant-2],"labels":["some label"]}'
          --input-dir /path/to/files
```

To use metadata from a file:

```shell
$ echo '{"tenants":["tenant-1","tenant-2],"labels":["some label"]}' > metadata.json
$ dart -p prod -e wm \
       forklift submit \
          --metadata-file metadata.json
          --input-dir /path/to/files
```

By default, `forklift submit` will look for `.meta` files whose base name corresponds to 
other files submitted from a directory:

```shell
$ echo 'Here is the text content that will be processed by dart' > /input-dir/file-1.txt
$ echo '{"tenants":["tenant-1","tenant-2],"labels":["some label"]}' > /input-dir/file-1.meta
$ dart -p prod -e wm forklift submit --input-dir /input-dir
```

Per-file metadata (`.meta`) can be ignored by using the `--ignore-meta-files` flag.

Finally, per-file metadata, metadata from a file, and metadata from a command line can be 
combined. This means that the files will be submitted with tenants and labels from all of 
these sources:

```shell
# Set common metadata for all files
$ echo '{"tenants":["common-tenant-1"],"labels":["common-label-1"]}' > metadata.json

# Set metadata for individual files
$ echo 'Here is the text content that will be processed by dart' > /input-dir/file-1.txt
$ echo '{"tenants":["tenant-1"],"labels":["label-1"]}' > /input-dir/file-1.meta

$ echo 'Second document to be processed by dart' > /input-dir/file-2.txt
$ echo '{"tenants":["tenant-2"],"labels":["label-2"]}' > /input-dir/file-1.meta

$ dart -p prod -e wm \
       forklift submit \
          --tenant common-tenant-2 \
          --label common-label-2 \
          --metadata-file metadata.json \
          --input-dir /input-dir
```

The commands above will result in the following documents:

|  doc  |                  labels                  |                   tenants                  |
|-------|------------------------------------------|--------------------------------------------|
|file-1 | common-label-1, common-label-2, label-1  | common-tenant-1, common-tenant-2, tenant-1 |
|file-2 | common-label-1, common-label-2, label-2  | common-tenant-1, common-tenant-2, tenant-2 |

## Retrieve documents

### CDR Archive

```shell
$ dart -p prod -e wm retrieve cdr-archive -o wm-cdr-archive.zip
```

### CDRs

To retrieve one or more individual cdrs:

```shell
$ dart -p prod -e wm retrieve cdrs \
    -o /path/to/output/dir \
    c9adf7f0eba6570ab09382ce02139286 \
    945bcecff5e8d7dc66332824fdeb2a3e
```

To retrieve cdrs using doc ids saved to a file:

```shell
# ids file must contain line-separated doc ids
$ echo c9adf7f0eba6570ab09382ce02139286 > ids.txt
$ echo 945bcecff5e8d7dc66332824fdeb2a3e >> ids.txt
$ dart -p prod -e wm retrieve cdrs \
    -f ids.txt \
    -o /path/to/output/dir
```

### Raw documents

Retrieving raw documents works the same way as cdrs, but with `retrieve raws` instead
of `retrieve cdrs`:

```shell
$ dart -p prod -e wm retrieve raws \
    -o /path/to/output/dir \
    c9adf7f0eba6570ab09382ce02139286 \
    945bcecff5e8d7dc66332824fdeb2a3e
```
or
```shell
# ids file must contain line-separated doc ids
$ echo c9adf7f0eba6570ab09382ce02139286 > ids.txt
$ echo 945bcecff5e8d7dc66332824fdeb2a3e >> ids.txt
$ dart -p prod -e wm retrieve raws \
    -f ids.txt \
    -o /path/to/output/dir
```

## Querying

### Search

You can run corpex using a query set on the command line, but it is easier to save a query 
to a file:

```shell
$ echo '{"queries":[{"query_type":"TEXT","bool_type":"MUST","queried_fields":["cdr.extracted_text"],"query_string":"some query string"}]}' \
    > query-file.json

$ dart corpex search -f query-file.json \
                     --page-size 5 \
                     --page 0 \
                     --tenant tenant-id
```

You can then overwrite certain query fields. For instance, to apply the same search
to a different tenant:
```shell
$ dart corpex search -f query-file.json \
                     --tenant tenant-1

$ dart corpex search -f query-file.json \
                     --tenant tenant-2
````

To page through the top 15 results, five at a time:
```shell
$ dart corpex search -f query-file.json \
                     --page-size 5 \
                     --page 0

$ dart corpex search -f query-file.json \
                     --page-size 5 \
                     --page 1

$ dart corpex search -f query-file.json \
                     --page-size 5 \
                     --page 1
```

If you just want to know how many docs match a search, use `corpex count`:

```shell
$ dart corpex count -f query-file.json \
                    -tenant some-tenant-id
```

### Shave

To generate a list of the top N doc-ids matching a given search, use the `corpex shave`
command:

To write the top 5000 results to a file:

```shell
$ dart -p prod -e wm corpex shave -f query-file.json 5000 > doc-ids.txt
```
to retrieve the documents, you can use the generated file as an input to `retrieve cdrs`:
```shell
$ dart -p prod -e wm retrieve cdrs -f doc-ids.txt -o /shaved-cdrs-dir
```

## Deployment/Provision

### Stand up new environment

The preferred pattern for deploying and provisioning DART infrastructure is to generate
configuration profiles for each environment and execute all infrastructure commands 
relative to one of these profiles.

To stand up a new environment, which we'll call `newenv`, first make a profile based on 
the profile for the AWS account where it will be deployed. In this case, we'll use `prod`.

```shell
$ dart -p prod \
       -e newenv \                         # Set environment name (this will be newenv.prod.dart.worldmodelers.com) \
       --deploy-profile dart-distributed \ # Set deployment profile, used by AWS cdk to determine services configuration
       --dart-version wm:2.0.188 \          # Set project id (e.g., wm-dart-pipeline or dev-dart-pipeline) and version (tag of docker image used for deployment)
       profiles add newenv                 # Env-specific profile should have same name as env
```

It now becomes unnecessary to include anything beyond `-p newenv` to run any deployment
or provision commands.

We can now deploy and provision the environment simply by calling:

```shell
$ dart -p newenv pipeline provision-deploy all
```

or to separate the provision and deployment steps:

```shell
$ dart -p newenv pipeline provision all
$ dart -p newenv pipeline deploy all
```

### Use existing environment

If someone else has already provisioned an environment, or if you provisioned one without 
creating a cli configuraiton profile for it, you can pull all the relevant configuration 
from AWS metadata by using the global `--query-metadata` flag:

To create a profile for `newenv`, for instance, you would do this:

```shell
$ dart -p prod -e newenv --query-metadata profiles add newenv
```

You can now use `-p newenv` to run infrastructure commands for `newenv`

### Get environment state

To see the state of all instances in an environment, run:

```shell
$ dart -p newenv pipeline info
```

### Stop and start environment

To stop:

```shell
$ dart -p newenv pipeline stop
```

And to start back up:

```shell
$ dart -p newenv pipeline start
```

This will restart all the services as well.

### Cleaning up

To terminate and remove all infrastructure:

```shell
$ dart -p newenv pipeline nuke
```

## Tenant management

### View tenants

```shell
$ dart -p prod -e wm tenants ls
```

### Add one or more tenants

```shell
$ dart -p prod -e wm tenants add new-tenant
```

### Remove one or more tenants

```shell
$ dart -p prod -e wm tenants rm new-tenant-1 new-tenant-2
```

### View documents in tenant

```shell
$ dart -p prod -e wm tenants docs ls
```

### Add documents to tenant

```shell
$ dart -p prod -e wm tenants docs add [DOC_ID_1, DOC_ID_2, ...]
```

### Remove documents from tenant

```shell
$ dart -p prod -e wm tenants docs rm [DOC_ID_1, DOC_ID_2, ...]
```

## User management

### View users

To list existing users:

```shell
$ dart -p prod -e wm users ls
```

To view their user data, include the `--view` flag:

```shell
$ dart -p prod -e wm users ls --view
```

You can also view one or more users' data individually as follows:

```shell
$ dart -p prod -e wm users view [user-name-1, user-name-2, ...]
```

### Add user

To add a user without any user data beyond their username:

```shell
$ dart -p prod -e wm users add [USER_NAME]
```

You can set user data using the command line:

```shell
$ dart -p prod -e wm users add \
       --first-name John \
       --last-name Doe \
       --email john.doe@email.com \
       --group tenant-id-1/leader \
       --group tenant-id-2/read-only \
       john-doe
```
Or you can set user data by providing the json:
```shell
$ dart -p prod -e wm users add \
       --metadata '{"first_name":"John","last_name":"Doe","email":"john.doe@email.com","groups":["tenant-id-1/leader","tenant-id-2/read-only"]}' \
       john-doe
```
Or via a file:
```shell
$ echo '{"first_name":"John","last_name":"Doe","email":"john.doe@email.com","groups":["tenant-id-1/leader","tenant-id-2/read-only"]}' \
   > john-doe.json

$ dart -p prod -e wm users add \
       --metadata-file john-doe.json \
       john-doe
```

You can include the user data file, the user data json string, and the user data options,
and `dart-cli` will merge the data prioritizing 1) cli options, 2) cli json string, and 
finally 3) the json file.

### Update user

Updating a user works the same way as `add`:

```shell
$ dart -p prod -e wm users update john-doe --metadata-file john-doe.json
```

Fields that are included either in json or via command line options will overwrite 
existing fields. All other fields will remain the same

If you include groups in your user data, it *will not add these to existing groups* but 
will overwrite that user's groups completely. To add a user to one or more group without 
changing its existing groups, there is a separate command:

```shell
$ dart -p prod -e wm users add-groups john-doe tenant-a/member tenant-b/leader
```

## Kafka

To enable integration with DART's kafka broker, you will need to provide kafka
credentials, which can be done in one of the following two ways:

```bash
$ dart -p prod --kafka-username [USERNAME] --kafka-password [PASSWORD] ...
```
or
```bash
$ dart -p prod --kafka-login [USERNAME]:[PASSWORD] ...
```

### Read messages

To read all messages (both key and value) from a topic:

```bash
$ dart -p [PROFILE] messages read dart.cdr.streaming.updates
```

To read only keys or only values:

```bash
$ dart -p prod messages read --no-value dart.cdr.streaming.updates
$ dart -p prod messages read --no-key dart.cdr.streaming.updates
```

Output to a file instead of `stdout`:

```bash
$ dart -p prod messages read -o ./msgs.txt dart.cdr.streaming.updates
```

DART-CLI's message reading command has flexible filtration functionality. Say there is
a topic named `some.topic` populated with messages in the following form:

```json
{
  "int-field": 5,
  "str-field": "some value",
  "obj-field": {
    "nest-int-field": 3234,
    "nest-str-field": "some other value"
  },
  "arr-field": [2, 4, 6, 8],
  "obj-arr-field": [
    { "nest-int-field": -433, "nest-bool-field": true },
    { "nest-int-field": 23852, "nest-bool-field": false }
  ]
}
```

It is possible to isolate any fields, whether top-level or nested, by using the 
`--incl` and `--excl` options. The following examples show how different usages show
how various usages of these options will transform the output of the above message. 

```bash
$ dart -p prod messages read --incl int-field
...
message-key
===========
{
  "int-field": 5
}
...

$ dart -p prod messages read some.topic --incl int-field --incl obj-field
...
message-key
===========
{
  "int-field": 5,
  "str-field": "some value"
}
...

$ dart -p prod messages read some.topic --excl obj-field --excl arr-field
...
message-key
===========
{
  "int-field": 5,
  "str-field": "some value",
  "obj-arr-field": [
    { "nest-int-field": -433, "nest-bool-field": true },
    { "nest-int-field": 23852, "nest-bool-field": false }
  ]
}
...

$ dart -p prod messages read some.topic --incl obj-field.nest-str-field
...
message-key
===========
{
  "obj-field.nest-str-field": "some other value"
}
...

# Select an index of an array
$ dart -p prod messages read some.topic --incl obj-arr-field.0.nest-bool-field
...
message-key
===========
{
  "obj-arr-field.0.nest-bool-field": true
}

# Map an array to a nested field
$ dart -p prod messages read some.topic --incl obj-arr-field.nest-bool-field
...
message-key
===========
{
  "obj-arr-field.nest-bool-field": [true, false]
}

# Exclude a nested field on an array of objects
$ dart -p prod messages read some.topic --excl obj-arr-field.nest-bool-field
...
message-key
===========
{
  "int-field": 5,
  "str-field": "some value",
  "obj-arr-field": [
    { "nest-int-field": -433 },
    { "nest-int-field": 23852 }
  ]
}
...
```
