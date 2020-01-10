from fabric.api import *


def do_pack():
    """documents do_pack
    """
    local("mkdir -p versions")
    local("tar -czvf versions/web_static_$(date '+%Y%m%d%H%M%S').tgz web_static")
