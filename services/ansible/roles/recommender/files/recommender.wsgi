#!/usr/bin/env python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
from recommenderserver.__main__ import app as application
