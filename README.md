# AppConfigs
[![license](https://img.shields.io/pypi/l/appconfigs.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/appconfigs.svg)](https://pypi.org/project/appconfigs/)
[![Build status](https://ci.appveyor.com/api/projects/status/d5vg8c704m1el8pc/branch/master?svg=true)](https://ci.appveyor.com/project/jnsebgosselin/appconfigs/branch/master)
[![codecov](https://codecov.io/gh/jnsebgosselin/appconfigs/branch/master/graph/badge.svg)](https://codecov.io/gh/jnsebgosselin/appconfigs)

**AppConfigs** is a small Python module that provides user configuration file management features for Python applications. It is based on the config module of [Spyder](https://www.spyder-ide.org/), the scientific Python development environment.

## Installation

`AppConfigs` can be installed with `pip` by running:

```commandlines
pip install appconfigs
```

## Requirements

- [appdirs](https://github.com/ActiveState/appdirs) : To retrieve the directory that your app should use for storing user data.

## Get it started

First, you need to create a new Python file (for example `my_conf.py`) in which you :

1. define the location where the user configuration files are going to be saved, 
2. provide default values for the preferences,
3. setup the main configuration instance that your app will use.

### Configuration file setup

Let start with a project structure like the one below with the configuration file `my_conf.py` located 
in the module `/config` .

```
__init__.py
my_app.py
/config
    | __init__.py
    | my_conf.py
```

The example below shows the content of the `/config/my_conf.py` file. 

```python
# =============================================================================
# MY_CONF.PY file content
# =============================================================================
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

# Define the configuration version.
CONF_VERSION = '1.0.0'

# IMPORTANT NOTES:
# 1. When the default value of a current option is changed, a
#    MINOR update in config version is required, e.g. from 3.0.0 to 3.1.0
# 2. When options that are no longer needed in your codebase are removed,
#    or if options are renamed, then a MAJOR update in config
#    version is required, e.g. from 3.0.0 to 4.0.0
# 3. When new options are added, no update in config version is necessary

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
### Using the configuration in application files

We import the main configuration instance where needed to access and
manage the preferences of our application. For example, to get the value
of `pref2` in `section1` from the `my_app.py` file, we would do:

```python
# =============================================================================
# MY_APP.PY file content
# =============================================================================
from .config.my_conf import CONF
my_value = CONF.get('section1', 'pref2')
print(my_value)
>>> 'blue'
```
Since no user defined value has been set yet for this preference,
the default value is returned as expected.

To set a new value for `pref2` in `section1`, we would simply do:
```python
# =============================================================================
# MY_APP.PY file content
# =============================================================================
from .config.my_conf import CONF
CONF.set('section1', 'pref2', 'red')
my_value = CONF.get('section1', 'pref2')
print(my_value)
>>> 'red'
```
### How it works

#### Versionning

**AppConfigs** supports multiple configurations at the same time. This feature is mainly used when dealing
with diverging configuration between different version of our application. Usually, version naming should follow this pattern:

1. If you want to **change** the default value of a current option, you need to
   do a MINOR update in config version, e.g. from 3.0.0 to 3.1.0
2. If you want to **remove** options that are no longer needed in our codebase,
   or if you want to **rename** options, then you need to do a MAJOR update in
   version, e.g. from 3.0.0 to 4.0.0
3. You don't need to touch this value if you're just adding a new option

#### Configuration storage

You can define where your application will store it's user data in any directory that you want, provided that the user has read and write access to it.

As shown in the example above, you can also use the utility function `get_config_dir` from the `appconfigs.base` module that uses the [appdirs](https://github.com/ActiveState/appdirs) package to automatically define the directory that your app should use for storing user data. By default, this directory is defined as :

##### On Windows 7 and above :
- If there is an application author: `C:\Users\[USERNAME]\AppData\Local\[APPLICATION_AUTHOR]\[APPLICATION_NAME]`
- If there is **no** application author: `C:\Users\[USERNAME]\AppData\Local\[APPLICATION_NAME]`

##### On Linux :
On Linux/Unix based OS, the config files are stored at : `~/.config/[APPLICATION_NAME]`

##### On Mac :
On macOS, the config files are stored at : `/Users/[USERNAME]/Library/Application Support/[APPLICATION_NAME]`

You can also define a **custom user config directory** for your application through an os environment variable named after that of you application in caps followed by the suffix `'_DIR'`. When a value for such a variable exists, `get_config_dir` will return that value instead of the default one. So for the example above, we could define a custom user config directory for our app named `my_app_name` in the os environment variable named `MY_APP_NAME_DIR`.
