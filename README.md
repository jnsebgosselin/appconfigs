# AppConfigs
[![license](https://img.shields.io/pypi/l/appconfigs.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/appconfigs.svg)](https://pypi.org/project/appconfigs/)
[![Build status](https://ci.appveyor.com/api/projects/status/d5vg8c704m1el8pc/branch/master?svg=true)](https://ci.appveyor.com/project/jnsebgosselin/appconfigs/branch/master)
[![codecov](https://codecov.io/gh/jnsebgosselin/appconfigs/branch/master/graph/badge.svg)](https://codecov.io/gh/jnsebgosselin/appconfigs)

**AppConfigs** is a small Python module that provides user configuration file management features for Python applications. It is based on the config module of [Spyder](https://www.spyder-ide.org/), the scientific Python development environment.
## How to install

Simply install `appconfigs` with the command :

```commandlines
pip install appconfigs
```

## How to use

First, you need to create a new Python file (`my_conf.py` for example) in which you :

1. define the location where the user configuration files are going to be saved, 
2. provide default values for the preferences,
3. setup the main configuration instance that your app will use.

### Configuration file setup

Let start with a project structure like the one below with the configuration file `my_conf.py` located 
in the folder `/config` .

```
__init__.py
main_app.py
/config
    | __init__.py
    | my_conf.py
/db_handler
    | __init__.py
    | my_beautiful_bd_handler.py 
    | postgresql_proxy.py
    | mysql_proxy.py
```

The example below shows the content of the `/conf/my_conf.py` file. 

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
### Using the configuration in application files

We import the main configuration instance where needed and
manage the preferences of our application.

For example, to get the value of `pref2` in `section1` and use it in our `main.py` file, we would do:

```python
# =============================================================================
# MAIN.PY file content
# =============================================================================
from conf.my_conf import CONF
my_value = CONF.get('section1', 'pref2')
print(my_value)
>>> 'blue'
```
Since no user defined value has been set yet for this preference,
the default value is returned as expected.

To set a new value for `pref2` in `section1`, we would simply do:
```python
# =============================================================================
# MAIN.PY file content
# =============================================================================
from conf.my_conf import CONF
my_value = CONF.get('section1', 'pref2')
print(my_value)
>>> 'blue'

CONF.set('section1', 'pref2', 'red')
my_value = CONF.get('section1', 'pref2')
print(my_value)
>>> 'red'
```

### Where is the configuration stored ???



