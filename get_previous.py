#!/usr/bin/env python3

import requests
import sys
import os



def get_previous(service_name):

    with open(service_name, 'r') as f:
        pipeline = f.read().strip('\n')

    url = "https://10.150.232.234:8154/go/api/pipelines/{pipeline}/history".format(pipeline=pipeline)
    r = requests.get(url, verify=False).json()
    return r["pipelines"][1]["build_cause"]["material_revisions"][0]["modifications"][0]["revision"][:7]


if __name__ == "__main__":
    sha = get_previous(sys.argv[1])
    with open("FROM_GITSHA.txt", "w") as from_gitsha:
        from_gitsha.write(sha)

