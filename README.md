# forked repo for custom workflow

These agent files are built and deployed to the devregistry via [gocd](https://devcd.arnoldclark.com)

The build context is removed i.e. `build/` dir and pulled from the forked repo when the build script is ran. The Rakefile is then invoked which puts in place the build context for the image then builds it. Note adding files to the build context for this repo requires adding them to the Rakefile.

`./auto_build.sh` is used by gocd to build the image within swarm. It should be edited unless you know what you're doing. 

`./local_build.sh` leverages the same Rakefile however it builds the image locally. The difference between the two is this is using the local docker daemon.

** The pipeline for this repo is currently paused so that we can control when agents are built. It's only to be unpaused when the files in the repo have been updated **

## GoCD and Agents

These files currently build one agent that is being used by the `docker_ansible` agent profile within gocd. However this could be extended. The agent image is build with a few custom additions

- /rollback.py: This is built in for calling rollback on any pipeline as long as the name of the caller is provided
- /.vault_pass.py: The ansilbe password file which is provided to the env via gocd secure variables
- id_rsa and known_hosts: A key for accessing github ssh:// for the vault repo. This will be extended to an account on github for production.
- auto_build and local_build scirpts: explained above. 

### The pipeline flow:

#### Build
- unencrypt the ssh files
- run the auto_build.sh
- grab the version of the IMAGEID
- tag the newly build IMAGEID with the name that'll be pushed to the registry
#### Release
- push to registry

The next time the `docker_ansible` agent profile is invoked it will use this newly created image build.

## Update procedure

To update an agent to a new release ensure that you change inplace the current version in the auto or local build.sh file. This include the build version part of the url where the new version is pulled from. This can be found by copying the link on the download page or from the alert bell within gocd home page when a new release is available. 

Test everything locally before unpausing the pipeline. When everything is running ensure after the upgrade that you update the version in the elastic profile section for the relevant profile that you want to use the new version. The old image is will be kept around for rollback.

** Note ** I'll also put this in the stack section of the swarm repo. When updating the server component to a new version the entire process is done internally within the new container and the chosen storage backend (volume mounts likely) the entire process can take up to 10-15 mins to complete all the necessary startup and migration operations. It's advised that you tail the logs to keep an eye on it. The service will become available in the [proxy](https://intprx.arnoldclark.com:4443/stats?admin) when the upgrade is complete. 
