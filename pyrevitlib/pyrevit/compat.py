"""python engine compatibility module.

Example:
    >>> from pyrevit.compat import IRONPY277
    >>> from pyrevit.compat import safe_strtype
"""

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

IPY2 = PY2 and sys.implementation.name == 'ironpython'
IRONPY273 = sys.version_info[:3] == (2, 7, 3)
IRONPY277 = sys.version_info[:3] == (2, 7, 7)
IRONPY278 = sys.version_info[:3] == (2, 7, 8)
IRONPY279 = sys.version_info[:3] == (2, 7, 9)
IRONPY2710 = sys.version_info[:3] == (2, 7, 10)
IRONPY2711 = sys.version_info[:3] == (2, 7, 11)

IPY3 = PY3 and sys.implementation.name == 'ironpython'
IRONPY340 = sys.version_info[:3] == (3, 4, 0)

CPY2 = PY2 and sys.implementation.name == 'cpython'
CPY3 = PY3 and sys.implementation.name == 'cpython'

#pylint: disable=import-error,unused-import
if PY3:
    __builtins__["unicode"] = str

if PY2:
    import _winreg as winreg
    import ConfigParser as configparser
    from collections import Iterable
    import urllib2 as urllib
elif PY3:
    import winreg as winreg
    import configparser as configparser
    from collections.abc import Iterable
    import urllib


#pylint: disable=C0103
safe_strtype = str
if PY2:
    # https://gist.github.com/gornostal/1f123aaf838506038710
    safe_strtype = lambda x: unicode(x)  #pylint: disable=E0602,unnecessary-lambda
