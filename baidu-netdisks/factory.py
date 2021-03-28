#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import time
import json
import signal
import robust_layer
import lxml.etree
import urllib.request
import mirrors.mirror_site_factory
from datetime import datetime


def main():
    with mirrors.mirror_site_factory.ApiClient() as sock:
        cfgDict = mirrors.mirror_site_factory.params["config"]

        # send add messages
        for item in cfgDict:
            if "name" not in item:
                raise Exception("no \"name\" field in mirror site configuration")
            if "username" not in item:
                raise Exception("no \"username\" field in mirror site configuration")
            if "password" not in item:
                raise Exception("no \"password\" field in mirror site configuration")
            if "path" not in item:
                item["path"] = "/"
            sock.add_mirror_site(_genMetadataXml(item["name"], "1d"), json.dumps(item))

        # sleep forever
        while True:
            signal.pause()


def _genMetadataXml(name, schedInterval):
    msId = "baidu-netdisk" + name

    buf = ''
    buf += '<mirror-site id="%s">\n' % (name)
    buf += '  <name>%s</name>\n' % (name)
    buf += '  <storage type="file"/>\n'
    buf += '  <advertiser type="httpdir"/>\n'
    buf += '  <updater>\n'
    buf += '    <executable>updater.py</executable>\n'
    buf += '    <schedule type="interval">%s</schedule>\n' % (schedInterval)
    buf += '  </updater>\n'
    buf += '</mirror-site>\n'
    return buf


def _genCfgJson(username, password, path):
    data = dict()
    data["username"] = username
    data["password"] = password
    data["path"] = path
    return json.dumps(data)


###############################################################################

if __name__ == "__main__":
    main()
