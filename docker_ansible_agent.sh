#!/usr/bin/env bash

: <<COMMENT
to list versions you can build:

GOCD_VERSION=17.5.0 \
GOCD_FULL_VERSION=17.5.0-5095 \
GOCD_GIT_SHA=ce5f115d1dc008fab6166ad220772949114a875f \
GOCD_AGENT_DOWNLOAD_URL=https://download.gocd.io/binaries/17.5.0-5095/generic/go-agent-17.5.0-5095.zip \
rake -T build_image
COMMENT


# current latest version over alpine 
GOCD_VERSION=17.5.0 \
GOCD_FULL_VERSION=17.5.0-5095 \
GOCD_GIT_SHA=ce5f115d1dc008fab6166ad220772949114a875f \
GOCD_AGENT_DOWNLOAD_URL=https://download.gocd.io/binaries/17.5.0-5095/generic/go-agent-17.5.0-5095.zip \
rake gocd-agent-alpine-3.5:build_image

# Grab new image ID and tag for testing
IMAGEID=$(docker image ls gocd-agent-alpine-3.5 -q)
docker tag $IMAGEID devregistry.arnoldclark.com/gocd/docker-ansible-agent-alpine-3.5:v17.5.0
