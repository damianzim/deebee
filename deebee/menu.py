#!/usr/bin/env python3
# vim: ts=2 sts=0 sw=2 tw=100 et

from abc import ABC, abstractmethod
from collections import OrderedDict, namedtuple
from typing import Callable

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

  @property
  def name(self):
    return "main"

# getpass.getpass(prompt='Password: ', stream=None) for getting password

def menu():
  ctx_main = CtxMain()
  ctx = ctx_main

  while True:
    line = input(f"{ctx.name}> ").strip()
    if len(line) == 0:
      continue
    if line == "exit":
      if ctx is ctx_main:
        break
      ctx = ctx_main
      continue
    if not ctx.handle(Line(line)):
      break

if __name__ == "__main__":
  menu()
