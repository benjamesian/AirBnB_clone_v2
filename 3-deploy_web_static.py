#!/usr/bin/python3

from fabric.api import *
from os.path import basename, splitext
from datetime import datetime
env.hosts = ['35.231.46.174', '35.185.29.97']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/holberton'


def do_pack():
    """compresses web_static/ as a timestamped .tgz
    """
    go_to = "versions/web_static_{}.tgz".format(
        datetime.now().strftime('%Y%m%d%H%M%S'))
    local("mkdir -p versions")
    local("tar -czvf {} web_static/".format(go_to))
    return go_to


def do_deploy(archive_path):
    """deploys web_static.tgz to web-01 & web-02
    """
    try:
        arch_w_ext = basename(archive_path)
        arch_base = splitext(arch_w_ext)[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("tar -xzf /tmp/{} -C {}".format(arch_w_ext, path))
        run("rm /tmp/{}".format(arch_w_ext))
        run("mv {1}web_static {1}{0}".format(arch_base, path))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{} /data/web_static/current".format(path, arch_base))
        return True
    except Exception:
        return False


def deploy():
    """compresses web_static/ & deploys to web-01 & web-02
    """
    return do_deploy(do_pack())
