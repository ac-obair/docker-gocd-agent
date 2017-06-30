#!/usr/bin/env bash

: <<COMMENT
to list versions you can build:

GOCD_VERSION=17.7.0 \
GOCD_FULL_VERSION=17.7.0-5095 \
GOCD_GIT_SHA=ce5f115d1dc008fab6166ad220772949114a875f \
GOCD_AGENT_DOWNLOAD_URL=https://download.gocd.io/binaries/17.5.0-5095/generic/go-agent-17.5.0-5095.zip \
rake -T build_image

To upgrade the agent replace all instances over 17.7.0 with the new version. 

Note the build version 0-5147 can be gotten from the gocd master server under the bell icon letting you know that theres a new release.
COMMENT


# current latest version over alpine 
GOCD_VERSION=17.7.0 \
GOCD_FULL_VERSION=17.7.0-5095 \
GOCD_GIT_SHA=ce5f115d1dc008fab6166ad220772949114a875f \
GOCD_AGENT_DOWNLOAD_URL=https://download.gocd.io/binaries/17.7.0-5147/generic/go-agent-17.7.0-5147.zip \
/usr/bin/rake gocd-agent-alpine-3.5:build_image

# Grab new image ID and tag for test
DOCKER_HOST="tcp://mrlswarm-bld01:2375" docker image ls --filter reference='*:v17.7.0' -q > IMAGEID.txt
