# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

# ---- Standard library imports
import os.path as osp

# ---- Third party library imports
from appdirs import AppDirs


def get_home_dir():
    """Return user home directory."""
    return osp.expanduser('~')


def get_config_dir(appname):
    """Return gwhat config directory."""
    dirs = AppDirs(appname, appauthor=False)
    return dirs.user_config_dir
