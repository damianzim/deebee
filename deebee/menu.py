#!/usr/bin/env python3
# vim: ts=2 sts=0 sw=2 tw=100 et

from abc import ABC, abstractmethod
from collections import OrderedDict, namedtuple
import getpass
import hashlib
from typing import Callable

from tabulate import tabulate

from deebee.model import ModelClient, ModelRestaurant

class Line:
  def __init__(self, line):
    self.iter = iter(line.split())

  def get_token(self, label=None):
    try:
      return next(self.iter)
    except StopIteration:
      if label is not None:
        print(f"Error: Missing {label}")
      return None

Cmd = namedtuple("Cmd", "args callback")

class Mgr:
  def __init__(self, conn):
    self.conn = conn
    self.ctx = None

class Ctx(ABC):
  def __init__(self, mgr):
    self.cmds = OrderedDict()
    self.cmds["help"] = Cmd("", self.help)
    self.mgr = mgr

  @property
  @abstractmethod
  def name(self):
    ...

  def handle(self, line):
    token = line.get_token("command")
    if token is None:
      return False
    if token not in self.cmds:
      print("Error: Command not found")
      return True
    self.cmds[token].callback(line)
    return True # ??

  def help(self, _):
    for name, (args, _) in self.cmds.items():
      print(f"?{name} {args}" if len(args) > 0 else f"?{name}")

class CtxMain(Ctx):
  def __init__(self, mgr):
    Ctx.__init__(self, mgr)
    self.cmds["login"] = Cmd("<email>", self.login)

  @property
  def name(self):
    return "main"

  def login(self, line):
    email = line.get_token("email")
    if email is None:
      return
    password = getpass.getpass(prompt="Password: ", stream=None)
    if len(password) == 0:
      print("Error: Password is empty")
      return
    password = hashlib.sha256(password.encode()).digest()
    with self.mgr.conn.cursor() as cursor:
      account_type = cursor.callfunc("ofoa_auth", str, [email, password])
    if account_type is None:
      print("Error: Invalid email or password")
      return
    if account_type == "client":
      self.mgr.ctx = Client(self.mgr, email)
    elif account_type == "restaurant":
      self.mgr.ctx = Restaurant(self.mgr, email)
    else:
      print(f"Error: Invalid account type: {account_type}")
      return

class Client(Ctx):
  def __init__(self, mgr, email):
    Ctx.__init__(self, mgr)
    self.cmds["list"] = Cmd("{restaurants}", self.client_list)
    self.model = ModelClient.login(mgr.conn, email)

  @property
  def name(self):
    return "client"

  def client_list(self, line):
    resource = line.get_token("resource")
    if resource is None:
      return
    conn = self.mgr.conn
    if resource == "restaurants":
      header, rows = self.model.list_restaurants()
    else:
      print(f"Error: Unknown resource: {resource}")
      return
    print(tabulate(rows, header, tablefmt="psql"))

class Restaurant(Ctx):
  def __init__(self, mgr, email):
    Ctx.__init__(self, mgr)
    self.model = ModelRestaurant.login(mgr.conn, email)

  @property
  def name(self):
    return "restaurant"

def menu(conn):
  mgr = Mgr(conn)
  ctx_main = CtxMain(mgr)
  mgr.ctx = ctx_main

  while True:
    line = input(f"{mgr.ctx.name}> ").strip()
    if len(line) == 0:
      continue
    if line == "exit":
      if mgr.ctx is ctx_main:
        break
      mgr.ctx = ctx_main
      continue
    if not mgr.ctx.handle(Line(line)):
      break

if __name__ == "__main__":
  menu(None)
