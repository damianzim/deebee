#!/usr/bin/env python3
# vim: ts=2 sts=0 sw=2 tw=100 et

from abc import ABC, abstractmethod
from collections import OrderedDict, namedtuple
import getpass
import hashlib
from typing import Callable

CURSOR = None
CTX = None

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

class Ctx(ABC):
  def __init__(self):
    self.cmds = OrderedDict()
    self.cmds["help"] = Cmd("", self.help)

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
  def __init__(self):
    Ctx.__init__(self)
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
    account_type = CURSOR.callfunc("ofoa_auth", str, [email, password])
    if account_type is None:
      print("Error: Invalid email or password")
      return
    global CTX
    if account_type == "client":
      CTX = Client()
    elif account_type == "restaurant":
      CTX = Restaurant()
    else:
      print(f"Error: Invalid account type: {account_type}")
      return

class Client(Ctx):
  def __init__(self):
    Ctx.__init__(self)

  @property
  def name(self):
    return "client"

class Restaurant(Ctx):
  def __init__(self):
    Ctx.__init__(self)

  @property
  def name(self):
    return "restaurant"

def menu(cursor):
  global CTX, CURSOR
  CURSOR = cursor
  ctx_main = CtxMain()
  CTX = ctx_main

  while True:
    line = input(f"{CTX.name}> ").strip()
    if len(line) == 0:
      continue
    if line == "exit":
      if CTX is ctx_main:
        break
      CTX = ctx_main
      continue
    if not CTX.handle(Line(line)):
      break

if __name__ == "__main__":
  menu(None)
