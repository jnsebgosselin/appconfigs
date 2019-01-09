# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

"""Installation script """

import setuptools
from setuptools import setup
from appconfigs import __version__, __project_url__

LONG_DESCRIPTION = ("The appconfig module provides user configuration file "
                    "management features for Python applications. "
                    "It is based on the config module of the Spyder project, "
                    "which is available at "
                    "https://github.com/spyder-ide/spyder).")

setup(name='appconfigs',
      version=__version__,
      description=("User configuration file management features "
                   "for Python applications."),
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      license='MIT',
      author='Jean-Sébastien Gosselin',
      author_email='jean-sebastien.gosselin@outlook.ca',
      url=__project_url__,
      ext_modules=[],
      packages=setuptools.find_packages(),
      package_data={},
      include_package_data=True,
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Microsoft :: OS Independent",
                   "Programming Language :: Python :: 3.6"],
      )
