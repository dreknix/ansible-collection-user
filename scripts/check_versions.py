#!/usr/bin/env python3

import configparser
import requests


versions = configparser.ConfigParser()

versions.read("playbooks/files/tools.cnf")

for section in versions.sections():
    if (versions.get(section, 'source') == "github"):
        name = versions.get(section, 'name')
        version = versions.get(section, 'version')
        try:
            response = requests.get("https://api.github.com/repos/" + name + "/releases/latest")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            result = response.json()
            if result:
                print("\033[91mRequest to GitHub failed: " + result["message"] + "\033[0m")
            raise SystemExit(err)
        latest = response.json()["tag_name"].split()[-1]
        if latest[0] == 'v':
            latest = latest[1:]
        if latest != version:
            print("\033[91m" + name + " " + version + " != " + latest + "\033[0m")
        else:
            print("\033[92m" + name + " " + version + "\033[0m")
    else:
        print("Unknown source: " + versions.get(section, 'source'))
