#!/usr/bin/env python
"""Create any missing database tables.

The app itself only calls create_tables() under `if __name__ == '__main__'`,
which never runs under gunicorn, so a fresh deployment has no tables until
this runs. Safe to re-run: peewee issues CREATE TABLE IF NOT EXISTS.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import mydb, TimelinePost

mydb.connect()
mydb.create_tables([TimelinePost])
mydb.close()

print("Database tables are up to date")
