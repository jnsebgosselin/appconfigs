# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Spyder Project Contributors
#
# This file is a derivative work of codes taken from the
# Spyder project, licensed under the terms of the MIT License.
# (https://github.com/spyder-ide/spyder)
# -----------------------------------------------------------------------------

"""
This module provides user configuration file management features for Python
applications. It is based on the ConfigParser class of the configparser
module, which is available in the standard library.
"""

# ---- Standard library imports
import os
import os.path as osp
import ast
import time
import configparser as cp
from distutils.version import StrictVersion
import shutil


class NoDefault:
    """Class that represents a default config value which is not set."""

    def __repr__(self):
        return '<default value not set>'


class DefaultsConfig(cp.ConfigParser):
    """Class used to save default config options to a file."""

    def __init__(self, name, path):
        cp.ConfigParser.__init__(self, interpolation=None)
        self.name = name
        self.path = path

    def _set(self, section, option, value, verbose):
        """
        Private set method
        """
        if not self.has_section(section):
            self.add_section(section)
        if verbose:
            print('%s[ %s ] = %s' % (section, option, value))
        cp.ConfigParser.set(self, section, option, value)

    def _write(self, filename):
        """
        Write file to disk.
        """
        with open(filename, 'w', encoding='utf-8') as inifile:
            self.write(inifile)

    def _save(self):
        """
        Save config into the associated .ini file
        """
        filename = self.get_filename()
        if not osp.exists(osp.dirname(filename)):
            os.makedirs(osp.dirname(filename))

        try:
            self._write(filename)
        except EnvironmentError:
            try:
                if osp.isfile(filename):
                    os.remove(filename)
                time.sleep(0.05)
                self._write(filename)
            except Exception as e:
                print("Failed to write user configuration file to disk, with "
                      "the exception shown below")
                print(e)

    def get_filename(self):
        """Return the name of the configuration file to use."""
        return osp.join(self.path, '{}.ini'.format(self.name))

    def set_defaults(self, defaults):
        """Set default config values."""
        for section, options in defaults:
            for option, new_value in options.items():
                self._set(section, option, new_value, False)

