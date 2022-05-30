#!/usr/bin/env python3
# vim: ts=2 sts=0 sw=2 tw=120 et

import os

import cx_Oracle as db

CONNECTION = None

def setup():
  global CONNECTION, CURSOR
  host, user, password = os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASS")
  CONNECTION = db.connect(dsn=host, user=user, password=password)

def close():
  global CONNECTION
  if CONNECTION is not None:
    CONNECTION.close()
