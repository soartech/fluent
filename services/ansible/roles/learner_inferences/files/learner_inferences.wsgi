#!/usr/bin/env python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
from learner_inferences_server.__main__ import app as application
