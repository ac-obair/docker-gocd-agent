#!/usr/bin/env python3

import requests
import sys
import os
from pprint import pprint as pp


def get_pipeline_name(f):

    # Either read the name from a file or stdin 
    # Note file seem to work best within the pipeline call

    try:
        with open(f, 'r') as service_name:
            return service_name.read().strip('\n')
    except TypeError:
        return f
    except FileNotFoundError:
        return f

def fetch_pipeline_data(service_name, avoid_recursion=None):
 
    # Build a url with with name of the pipeline you wish to query

    url = "https://10.150.232.234:8154/go/api/pipelines/{pipeline}/history".format(pipeline=service_name)
    print(url) 
    # sessions persist meta data for a connection across calls
    req = requests.Session()
    req.auth = ("agent", os.environ["AGENT_PASSWORD"])
    #req.auth = ("lighiche", os.environ["MY_PASS"])
    result = req.get(url, verify=False).json()
    
    if avoid_recursion:
        return result

    return return_last_successful_deploy(result)

def check_pipeline_type(result):

    # Pipelines with git material use SHA as their revision.
    # Whereas deployment pipelines depend on material from other pipelines
    # These use pipelines/label/stage/counter for revision. We must parse this out and rerun the request.

    # This logic is implemented to keep functionality for parsing both types of material name 
    # Following CI/CD logic the last successfully build image should've been the last to run in prod
   
    check_material = result["pipelines"][0]["build_cause"]["material_revisions"][0]["modifications"][0]["revision"]

    try:
        return fetch_pipeline_data(check_material[:check_material.index('/')], True)
    except ValueError:
        # modify nothing if there's no / in the revision name
        return result

def return_last_successful_deploy(result): 
    result = check_pipeline_type(result)
  
    # history for 10 pipelines kept
    for index in range(1, len(result["pipelines"])):
        # Get label and release revision for last 10 deploys, if new pipeline IndexError is caught
        revision = result["pipelines"][index]["build_cause"]["material_revisions"][0]["modifications"][0]["revision"]
      
        label = int(result["pipelines"][index]["label"])

        try: 
            rev = revision.index('/')
        except ValueError:
            rev = revision[:7]

        print("Checking for last successful deploy:  stages for label {label} on {rev}".format(label=label, rev=rev))

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
        print("A gitsha for a fully successful build wasn't returned from function 'return_last_successful_deploy' this is probably because there hasn't been one yet. Is this a new pipeline? This logic has been tested, try looking at the json() dump from the req call.")
        raise(err)
