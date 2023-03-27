#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
# file compression


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.
    """
    try:
        local("mkdir -p versions")

        now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_name = "web_static_{}.tgz".format(now)

        local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except IOError:
        return None
