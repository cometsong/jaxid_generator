from __future__ import print_function

from nose.tools import *
import jaxid_generator

def setup():
    """set up test fixtures"""
    print("SETUP!")

def teardown():
    """tear down test fixtures"""
    print("TEAR DOWN!")

#@with_setup(setup, teardown)
def test_basic():
    """test nosetests running"""
    print("I RAN!")
