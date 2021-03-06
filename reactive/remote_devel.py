#!/usr/bin/python3
# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Leonardo Arias
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess

from charms.reactive import when_not, set_state
from charmhelpers import fetch
from charmhelpers.core import (
    hookenv,
    host
)


_USERNAME = 'ubuntu'
_HOME = os.path.join('/home', _USERNAME)
_DOTFILES_REPO = 'https://github.com/elopio/dotfiles'


@when_not('remote-devel.installed')
def install_remote_devel():
    os.makedirs(os.path.join(_HOME, 'workspace'), exist_ok=True)
    _install_utils()
    _install_source_control()
    _install_projects()
    _install_dotfiles()
    host.chownr(
        _HOME, owner=_USERNAME, group=_USERNAME,
        follow_links=True, chowntopdir=True)
    set_state('remote-devel.installed')


def _install_utils():
    fetch.apt_install('emacs-nox')
    # dictionaries
    fetch.apt_install('aspell-es')
    fetch.apt_install('byobu')
    _install_mosh()


def _install_mosh():
    fetch.apt_install('mosh')
    hookenv.open_port('60000-61000', 'UDP')


def _install_source_control():
    fetch.apt_install('git')
    fetch.apt_install('bzr')


def _install_projects():
    _install_snapcraft()
    _install_go()


def _install_snapcraft():
    fetch.apt_install('lxd')
    fetch.apt_install('snapcraft')


def _install_go():
    fetch.apt_install('golang-go')
    os.makedirs(os.path.join(_HOME, 'workspace', 'go'), exist_ok=True)


def _install_dotfiles():
    dotfiles_workspace = os.path.join(_HOME, 'workspace', 'dotfiles')
    subprocess.check_call(['git', 'clone', _DOTFILES_REPO, dotfiles_workspace])
    subprocess.check_call(
        ['env', 'HOME=' + _HOME,
         os.path.join(dotfiles_workspace, 'install.sh'),
         'devel'])
    subprocess.check_call(
        ['git', 'remote', 'set-url', 'origin',
         'git@github.com:elopio/dotfiles'],
        cwd=dotfiles_workspace)
