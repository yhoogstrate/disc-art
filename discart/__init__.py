#!/usr/bin/env python
# *- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 textwidth=79:


import logging
import sys

__version_info__ = ('0', '0', '2')
__version__ = '.'.join(__version_info__) if (len(__version_info__) == 3) else '.'.join(__version_info__[0:3]) + "-" + __version_info__[3]
__author__ = 'Youri Hoogstrate'
__homepage__ = 'https://github.com/yhoogstrate/disc-art'
__license__ = 'GNU General Public License v3 (GPLv3)'
__license_notice__ = 'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.'

__log_format__ = "[%(filename)s:%(lineno)s - %(funcName)s()] %(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=__log_format__, stream=sys.stderr)
log = logging.getLogger(__name__)
