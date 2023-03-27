#!/usr/bin/python3
from fabric.api import env, run, put
import os
# using fabric to automate

env.hosts = ['54.242.117.7', '54.226.19.77']
env.user = 'ubuntu'
env.key_filename = '/.ssh'


def do_deploy(archive_path):
    """
    distribute zip
    """
    if not os.path.exists(archive_path):
        return False
    archive_name = os.path.basename(archive_path)
    archive_name_without_ext = os.path.splitext(archive_name)[0]
    put(archive_path, '/tmp/')
    run("mkdir -p /data/web_static/releases/{}/"
        .format(archive_name_without_ext))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
        .format(archive_name, archive_name_without_ext))
    run("rm /tmp/{}".format(archive_name))
    run("mv /data/web_static/releases/{}/web_static/* \
         /data/web_static/releases/{}/"
        .format(archive_name_without_ext, archive_name_without_ext))
    run("rm -rf /data/web_static/releases/{}/web_static"
        .format(archive_name_without_ext))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(archive_name_without_ext))

    return True
