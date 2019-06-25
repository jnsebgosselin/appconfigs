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


def get_config_dir(appname, appauthor=False):
    """
    Get and return the application config directory.

    :type appname: str
    :param appname: Application name.
    :param appauthor: Application author. By default, this value is set
        to False.
    :rtype: str
    :return: Return full path to the user-specific config dir for
        this application.
    """
    dirs = AppDirs(appname, appauthor=appauthor)
    return dirs.user_config_dir
