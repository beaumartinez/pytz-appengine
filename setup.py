#!/usr/bin/env python

import json
import sys
import urllib2

from distutils.command.install import install as _install
from distutils.core import setup
from setuptools import find_packages
from subprocess import call


class Install(_install):

    def run(self):
        _install.run(self)

        try:
            data = urllib2.urlopen('https://pypi.python.org/pypi/pytz/json').read()
            data = json.loads(data)
        except Exception:
            print 'Could not fetch latest pytz version! Falling back to default'
        else:
            latest_version = data['info']['version']
            releases = data['releases'][latest_version]

            release_url = None

            for release in releases:
                if release['url'].endswith('.zip'):
                    release_url = release['url']

            call_args = [sys.executable, 'build.py', 'all', '--dir', self.install_libbase]

            if release_url:
                call_args.extend(['--release-url', release_url])

            self.execute(lambda dir: call(call_args), (self.install_lib,), msg='Running post install task...')


setup(
    name='pytz-appengine',
    packages=find_packages(),
    cmdclass={'install': Install},
)
