import winapps
import os
import distro

browsers = ['Chrome', 'Firefox', 'Safari', 'Opera', 'Edge', 'Internet Explorer']
def get_from_linux():
    commands = {
        'debian': ('dpkg', '-l'),
        'ubuntu': ('dpkg', '-l'),
        'fedora': ('rpm', '-qa'),
        'arch': ('pacman', '-Q'),
        'slackware' : ('slapt-get', '--installed')
    }

    linux_distro = distro.linux_distribution(full_distribution_name=False)[0]
    like_distro =  distro.like()
