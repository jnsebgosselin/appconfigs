# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

# ---- Standard library imports
import os
import os.path as osp

# ---- Third party library imports
from appdirs import AppDirs


def get_home_dir():
    """
    Return user home directory.

    Returns
    -------
    str
        The full path to the user home directory.
    """
    return osp.expanduser('~')


def get_config_dir(appname: str, appauthor: bool = False) -> str:
    """
    Get and return the application config directory.

    Parameters
    ----------
    appname: str
        The name of the application for which the config directory is fetched.
    appauthor: str
        The name of the author or distributing body for this application
        (only used on Windows). Typically it is the owning company name.
        You may pass False to disable it.

    Returns
    -------
    str
     The full path to the user-specific config dir for this application.
    """
    config_dir = (os.environ.get(appname.upper() + '_DIR') or
                  AppDirs(appname, appauthor=appauthor).user_config_dir)

    return config_dir
