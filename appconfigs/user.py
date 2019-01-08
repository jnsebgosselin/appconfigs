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

