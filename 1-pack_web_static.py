#!/usr/bin/python3

from fabric.api import *


def do_pack():
    """compresses web_static/ as a timestamped .tgz
    """
    go_to = "versions/web_static_$(date '+%Y%m%d%H%M%S').tgz"
    local("mkdir -p versions")
    local(
        "tar -czvf {} web_static/".format(go_to))
