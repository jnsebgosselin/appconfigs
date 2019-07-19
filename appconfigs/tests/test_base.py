# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

# ---- Standard imports
import os
import os.path as osp

# ---- Third party imports
import pytest

# ---- Local imports
from appconfigs.base import get_config_dir

APPNAME = 'appconfigs_base_test'


# =============================================================================
# ---- Tests
# =============================================================================
@pytest.mark.parametrize("appauthor", [False, 'john_doe'])
def test_get_config_dir_default(appauthor):
    """
    Test that the path returned by get_config_dir has the correct basename
    and takes into account the value passed for the appauthor on Windows.
    """
    config_dir = get_config_dir(APPNAME, appauthor)

    assert config_dir
    assert not osp.exists(config_dir)
    assert osp.basename(config_dir) == APPNAME
    if appauthor and os.name == 'nt':
        assert osp.basename(osp.dirname(config_dir)) == appauthor


def test_get_config_dir_environ_var(tmpdir):
    """
    Test that the get_config_dir returns the path defined in the os
    environment variable when it exists for the specified application.
    """
    os.environ[APPNAME.upper() + '_DIR'] = str(tmpdir)

    config_dir = get_config_dir(APPNAME)
    assert osp.samefile(config_dir, str(tmpdir))


if __name__ == "__main__":
    pytest.main(['-x', osp.basename(__file__), '-vv', '-rw', '-s'])
