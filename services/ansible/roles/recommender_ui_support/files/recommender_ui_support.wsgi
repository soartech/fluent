#!/usr/bin/env python3
import sys
import logging
import swagger_server

logging.basicConfig(stream=sys.stderr)
from swagger_server.__main__ import app as application
