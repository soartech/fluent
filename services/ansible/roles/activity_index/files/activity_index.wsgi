#!/usr/bin/env python3
import sys
import logging
import activity_index_server

logging.basicConfig(stream=sys.stderr)
from activity_index_server.__main__ import app as application
