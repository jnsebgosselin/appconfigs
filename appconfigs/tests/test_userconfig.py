# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

# ---- Standard imports
import os.path as osp
import filecmp

# ---- Third party imports
import pytest

# ---- Local imports
from appconfigs.user import UserConfig

NAME = 'user_config_tests'
CONF_VERSION = '0.1.0'
DEFAULTS = [
    ('main',
        {'first_option': 'value',
         'second_option': 24.567,
         'third_option': 22,
         'fourth_option': True}
     )
]


# ---- Pytest fixtures
@pytest.fixture
def configdir(tmpdir):
    return osp.join(str(tmpdir), 'UserConfigTests')

