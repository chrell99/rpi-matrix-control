import os
from bottle import template

def setup_index(app):
    return template("Defaultpage")