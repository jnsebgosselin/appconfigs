# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

# ---- Standard imports
import os.path as osp
import filecmp
import configparser as cp

# ---- Third party imports
import pytest

# ---- Local imports
from appconfigs.user import UserConfig, NoDefault

NAME = 'user_config_tests'
CONF_VERSION = '0.1.0'
DEFAULTS = [
    ('main',
        {'option#1': 'value',
         'option#2': '24.567',
         'option#3': 24.567,
         'option#4': 22,
         'option#5': True,
         'option#6': ['value', 22, 24.567, True],
         'option#7': ('value', 22, 24.567, True),
         'option#8': {'suboption': ('value',  24.567)},
         }
     )
]


# ---- Pytest fixtures
@pytest.fixture
def configdir(tmpdir):
    return osp.join(str(tmpdir), 'UserConfigTests')


# ---- Tests
@pytest.mark.parametrize("backup_value", [True, False])
def test_files_creation(configdir, backup_value):
    """
    Test that the .ini, .bak, and default files are created as expected in the
    specified app config directory.
    """
    conf = UserConfig(NAME, defaults=DEFAULTS, load=True, path=configdir,
                      backup=backup_value, version=CONF_VERSION, raw_mode=True)

    assert conf.get_filename() == osp.join(configdir, NAME + '.ini')
    assert osp.exists(conf.get_filename())
    assert osp.exists(osp.join(conf.path, 'defaults'))
    assert osp.exists(osp.join(conf.path, 'defaults', 'defaults-0.1.0.ini'))
    assert osp.exists(conf.get_filename() + '.bak') is False

    # Init UserConfig a second time to trigger the creation of a backup file.
    conf = UserConfig(NAME, defaults=DEFAULTS, load=True, path=configdir,
                      backup=backup_value, version=CONF_VERSION, raw_mode=True)

    assert osp.exists(conf.get_filename() + '.bak') is backup_value
    if backup_value is True:
        assert filecmp.cmp(conf.get_filename(), conf.get_filename() + '.bak',
                           shallow=False)


def test_get_values(configdir):
    """
    Test that values are returned correctly with the right type.
    """
    conf = UserConfig(NAME, defaults=DEFAULTS, load=True, path=configdir,
                      backup=True, version=CONF_VERSION, raw_mode=True)

    for section, options in DEFAULTS:
        for option, value in options.items():
            assert conf.get(section, option) == value
            assert conf.get_default(section, option) == value

    # Get a value of an option that does not exists without providing a
    # default value.
    assert conf.get_default('main', 'dummy') is NoDefault
    with pytest.raises(cp.NoOptionError):
        conf.get('main', 'dummy')

    # Get a value of an option that does not exists while providing a
    # default value.
    assert conf.get_default('main', 'dummy') is NoDefault
    assert conf.get('main', 'dummy', 8.234) == 8.234
    assert conf.get_default('main', 'dummy') == 8.234

    # Get a value from section that does not exists without providing a
    # default value.
    assert conf.get_default('dummy', 'dummy') is NoDefault
    with pytest.raises(cp.NoSectionError):
        conf.get('dummy', 'dummy')

    # Get a value from section that does not exists while providing a
    # default value.
    assert conf.get_default('dummy', 'dummy') is NoDefault
    assert conf.get('dummy', 'dummy', 'new_value') == 'new_value'
    assert conf.get_default('dummy', 'dummy') == 'new_value'


def test_set_values(configdir, mocker):
    """
    Test that values are set correctly with the right type corresponding to
    that of their default values if any.
    """
    conf = UserConfig(NAME, defaults=DEFAULTS, load=True, path=configdir,
                      backup=True, version=CONF_VERSION, raw_mode=True)

    # Set the value of options with default value.
    params = [
        ('main', 'option#1', 34.678, '34.678'),
        ('main', 'option#3', 34.678, 34.678),
        ('main', 'option#4', 34.678, 34),
        ('main', 'option#5', '', False),
        ('main', 'option#5', 34.678, True),
        ]

    mocked_save = mocker.patch('appconfigs.user.UserConfig._save')
    for i, (section, option, new_value, expected_value) in enumerate(params):
        conf.set(section, option, new_value)
        assert conf.get(section, option) == expected_value
        assert mocked_save.call_count == i + 1

    # Set the value of new options with no default value.
    params = [
        ('main', 'new_option', 'some_str'),
        ('new_section', 'new_option', 12.123),
        ]

    mocked_save.reset_mock()
    for i, (section, option, new_value) in enumerate(params):
        assert conf.get_default(section, option) is NoDefault

        conf.set(section, option, new_value)
        assert conf.get(section, option) == new_value
        assert conf.get_default(section, option) is new_value
        assert mocked_save.call_count == i + 1



if __name__ == "__main__":
    pytest.main(['-x', osp.basename(__file__), '-v', '-rw', '-s'])
