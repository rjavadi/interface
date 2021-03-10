#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/cs/websites/hri-study.cs.sfu.ca/ss-study/')
from app import app as application
# application.secret_key = 'anything you wish'

