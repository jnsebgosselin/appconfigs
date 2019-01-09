# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

"""
File for running tests programmatically.
"""

import pytest


def main():
    """
    Run pytest tests.
    """
    errno = pytest.main(['-x', 'appconfigs',  '-v', '-rw', '--durations=10',
                         '--cov=appconfigs'])
    if errno != 0:
        raise SystemExit(errno)


if __name__ == '__main__':
    main()
