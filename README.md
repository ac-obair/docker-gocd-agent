# forked repo for custom workflow

These agent files are built and deployed to the devregistry via [gocd](https://devgocd.arnoldclark.com)

The build context is removed i.e. `build/` dir and pulled from the forked repo when the build script is ran. The Rakefile is then invoked which puts in place the build context for the image then builds it. Note adding files to the build context for this repo requires adding them to the Rakefile.

`./auto_build.sh` is used by gocd to build the image within swarm. It should be edited unless you know what you're doing. 

`./local_build.sh` leverages the same Rakefile however it builds the image locally. The difference between the two is this is using the local docker daemon.

** The pipeline for this repo is currently paused so that we can control when agents are built. It's only to be unpaused when the files in the repo have been updated **
