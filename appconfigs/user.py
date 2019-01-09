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
import copy


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
        if not isinstance(value, str):
            value = repr(value)
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
                self.cleanup()
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

    def cleanup(self):
        """Remove .ini file associated to config."""
        if osp.isfile(self.get_filename()):
            os.remove(self.get_filename())


class UserConfig(DefaultsConfig):
    """UserConfig class based on ConfigParser."""

    def __init__(self, name, defaults=None, load=True, version=None,
                 path=None, backup=False, raw_mode=False):
        DefaultsConfig.__init__(self, name, path)
        self.raw = 1 if raw_mode else 0
        self.backup = backup

        self.defaults = copy.deepcopy(defaults)
        if defaults is not None:
            self.reset_to_defaults(save=False)
        self._create_backup()

        if load:
            # Override Default options if config file exists.
            self.read(self.get_filename(), encoding='utf-8')
            self._save_new_defaults(defaults, version, path)

            if defaults is None:
                # If no defaults are defined, set .ini file settings as default
                self.set_as_defaults()

            # Update Default options only if major/minor version is different.
            self._check_version(version)
            old_version = self.get_version(version)
            if StrictVersion(version) != StrictVersion(old_version):
                self._create_backup(version=old_version)
                self._update_defaults(defaults, old_version)
                self._remove_deprecated_options(old_version)
                self.set_version(version, save=False)

    def get_version(self, version='0.0.0'):
        """Return configuration (not application!) version."""
        return self.get('main', 'version', version)

    def set_version(self, version='0.0.0', save=True):
        """Set configuration (not application!) version"""
        self._check_version(version)
        self.set('main', 'version', version, save=save)

    @staticmethod
    def _check_version(version):
        """
        Check that the format of version is as expected.
        """
        warning = ("Version number is incorrect: it must be a string "
                   "with the X.Y.Z format.")
        try:
            version = StrictVersion(version)
        except (ValueError, TypeError):
            raise ValueError(warning)
        else:
            return True

    def _load_old_defaults(self, old_version):
        """Read old defaults."""
        path = osp.join(
            self.path, 'defaults', 'defaults-' + old_version + '.ini')
        old_defaults = cp.ConfigParser()
        old_defaults.read(path)
        return old_defaults

    def _save_new_defaults(self, defaults, new_version, path):
        """Save new defaults."""
        new_defaults = DefaultsConfig(name='defaults-' + new_version,
                                      path=osp.join(path, 'defaults'))
        if not osp.isfile(new_defaults.get_filename()):
            new_defaults.set_defaults(defaults)
            new_defaults._save()

    def _create_backup(self, version=None):
        """Create a backup of the current config file."""
        if self.backup is True:
            ini_fname = self.get_filename()
            bak_fname = ("{}.bak".format(ini_fname) if version is None else
                         "{}-{}.bak".format(ini_fname, version))
            try:
                shutil.copyfile(ini_fname, bak_fname)
            except IOError:
                pass

    def _update_defaults(self, defaults, old_version, verbose=False):
        """Update defaults after a change in version"""
        old_defaults = self._load_old_defaults(old_version)
        for section, options in defaults:
            for option, new_value in options.items():
                try:
                    old_value = old_defaults.get(section, option)
                except Exception:
                    old_value = None
                if old_value is None or str(new_value) != old_value:
                    self._set(section, option, new_value, verbose)

    def _remove_deprecated_options(self, old_version):
        """
        Remove options which are present in the .ini file but not in defaults
        """
        old_defaults = self._load_old_defaults(old_version)
        for section in old_defaults.sections():
            for option, _ in old_defaults.items(section, raw=self.raw):
                if self.get_default(section, option) is NoDefault:
                    try:
                        self.remove_option(section, option)
                        if len(self.items(section, raw=self.raw)) == 0:
                            self.remove_section(section)
                    except cp.NoSectionError:
                        self.remove_section(section)

    def set_as_defaults(self):
        """Set defaults from the current config."""
        self.defaults = []
        for section in self.sections():
            secdict = {}
            for option, value in self.items(section, raw=self.raw):
                try:
                    value = ast.literal_eval(value)
                except (SyntaxError, ValueError):
                    pass
                secdict[option] = value
            self.defaults.append((section, secdict))

    def reset_to_defaults(self, save=True, verbose=False, section=None):
        """Reset config to Default values"""
        for sec, options in self.defaults:
            if section is None or section == sec:
                for option, value in options.items():
                    self._set(sec, option, value, verbose)
        if save:
            self._save()

    def get_default(self, section, option):
        """
        Get Default value for a given section and option.
        (This method is useful for type checking in 'get' method)
        """
        for sec, options in self.defaults:
            if sec == (section or 'main') and option in options:
                return options[option]
        else:
            return NoDefault

    def set_default(self, section, option, default_value):
        """Set Default value for a given section and option."""
        for sec, options in self.defaults:
            if sec == (section or 'main'):
                options[option] = default_value
                break
        else:
            self.defaults.append(
                (section, {option: default_value}))

    def get(self, section, option, default=NoDefault):
        """Get an option from the specified section."""
        if not self.has_section(section):
            if default is NoDefault:
                raise cp.NoSectionError(section)
            else:
                self.add_section(section)

        if not self.has_option(section, option):
            if default is NoDefault:
                raise cp.NoOptionError(option, section)
            else:
                self.set(section, option, default)
                return default

        value = cp.ConfigParser.get(self, section, option, raw=self.raw)

        # Use type of default_value to parse value correctly
        default_value = self.get_default(section, option)
        if not isinstance(default_value, str):
            try:
                value = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                pass
        return value

    def set(self, section, option, value, verbose=False, save=True):
        """Set an option for the specified section."""
        default_value = self.get_default(section, option)
        if default_value is NoDefault:
            default_value = value
            self.set_default(section, option, default_value)
        if isinstance(default_value, bool):
            value = bool(value)
        elif isinstance(default_value, int):
            value = int(value)
        elif isinstance(default_value, float):
            value = float(value)
        elif isinstance(default_value, str):
            value = str(value)
        self._set(section, option, value, verbose)
        if save:
            self._save()

    def remove_section(self, section):
        """Remove the section from the configs and save to file."""
        cp.ConfigParser.remove_section(self, section)
        self._save()

    def remove_option(self, section, option):
        """
        Remove the option in the specified section from the configs and
        save to file.
        """
        cp.ConfigParser.remove_option(self, section, option)
        self._save()
