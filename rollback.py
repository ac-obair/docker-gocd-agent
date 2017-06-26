#!/usr/bin/env python3

import requests
import sys
import os
from pprint import pprint as pp


def get_pipeline_name(f):

    with open(f, 'r') as service_name:
        return service_name.read().strip('\n')


def fetch_pipeline_data(service_name):

    url = "https://10.150.232.234:8154/go/api/pipelines/{pipeline}/history".format(pipeline=service_name)
    # sessions persist meta data for a connection across calls
    req = requests.Session()
    req.auth = ("agent", os.environ["AGENT_PASSWORD"])
    #req.auth = ("lighiche", "")

    result = req.get(url, verify=False).json()
 
    return return_last_successful_deploy(result)


def return_last_successful_deploy(result): 

    # history for 10 pipelines kept
    for index in range(1, len(result["pipelines"])):

        # Get label and release revision for last 10 deploys, if new pipeline IndexError is caught
        revision = result["pipelines"][index]["build_cause"]["material_revisions"][0]["modifications"][0]["revision"]
        label = int(result["pipelines"][index]["label"])

        print("Checking for last successful deploy:  stages for label {label} on {rev}".format(label=label, rev=revision[:7]))

        # Parse number of stages for last 10 deploys, if new pipeline IndexError is caught
        stage_len = len(result["pipelines"][index]["stages"])

        # Stages NOT recorded after first if Failed, if len(stages) ran with result Passed, select last successful deploy
        for stages in range(0, stage_len):
            stage = result["pipelines"][index]["stages"][stages]

            try:
                if "Passed" in stage["result"]:
                    if stages == (stage_len -1):
                        return revision[:7]

            except KeyError:
                continue


if __name__ == "__main__":

    sha = fetch_pipeline_data(get_pipeline_name(sys.argv[1]))

    try:
        with open("FROM_GITSHA.txt", "w") as gitsha:
            gitsha.write(sha)
    except TypeError as err:
        print("The gitsha wasn't returned from function 'return_last_successful_deploy' this is probably because there hasn't been one yet. Is this a new pipeline? This logic has been tested, try looking at the json() dump from the req call.")
        raise(err)
