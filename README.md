# AppConfigs
[![license](https://img.shields.io/pypi/l/appconfigs.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/appconfigs.svg)](https://pypi.org/project/appconfigs/)
[![Build status](https://ci.appveyor.com/api/projects/status/d5vg8c704m1el8pc/branch/master?svg=true)](https://ci.appveyor.com/project/jnsebgosselin/appconfigs/branch/master)
[![codecov](https://codecov.io/gh/jnsebgosselin/appconfigs/branch/master/graph/badge.svg)](https://codecov.io/gh/jnsebgosselin/appconfigs)

**AppConfigs** is a small Python module that provides user configuration file management features for Python applications. It is based on the config module of [Spyder](https://www.spyder-ide.org/), the scientific Python development environment.

## How to use

First, we create a new Python file in which we (1) define the location
where the user configuration files are going to be saved, (2) provide default
values for the preferences and (3) setup the main configuration instance that
we are going use in our app.

This is an example of how this file should look like:

```python
from appconfigs.user import UserConfig
from appconfigs.base import get_config_dir

# Define the location where the user configuration files are going to be saved
# (you can use any other location with write permission if you want).
CONFIG_DIR = get_config_dir('my_app_name')

# Provide default values for the preferences.
DEFAULTS = [
    ('main',
        {'pref1': '14px',
         'pref2': 'french'}
     ),
    ('section1',
        {'pref1': 104,
         'pref2': 'blue'}
     )
    ('section2',
        {'pref1': True}
     )
]

# =============================================================================
# Config instance
# =============================================================================
# IMPORTANT NOTES:
# 1. If you want to *change* the default value of a current option, you need to
#    do a MINOR update in config version, e.g. from 3.0.0 to 3.1.0
# 2. If you want to *remove* options that are no longer needed in our codebase,
#    or if you want to *rename* options, then you need to do a MAJOR update in
#    version, e.g. from 3.0.0 to 4.0.0
# 3. You don't need to touch this value if you're just adding a new option
CONF_VERSION = '1.0.0'

# Setup the main configuration instance.
try:
    CONF = UserConfig('my_app_name', defaults=DEFAULTS, load=True,
                      version=CONF_VERSION, path=CONFIG_DIR,
                      backup=True, raw_mode=True)
except Exception:
    CONF = UserConfig('my_app_name', defaults=DEFAULTS, load=False,
                      version=CONF_VERSION, path=CONFIG_DIR,
                      backup=True, raw_mode=True)

```

Then, we import the main configuration instance where we need it to
manage the preferences of our application.

For example, to get the value of pref2 in section1, we would do:
```
>>> from <path>.<to>.<our>.<config>.<file> import CONF
>>> CONF.get('section1', 'pref2')
'blue'
```
Since no user defined value has been set yet for this preference,
the default value is returned as expected.

To set a new value for pref2 in section1, we would simply do:
```
>>> from <path>.<to>.<our>.<config>.<file> import CONF
>>> CONF.set('section1', 'pref2', 'red')
>>> CONF.get('section1', 'pref2')
'red'
```

