#!/usr/bin/env python3
# vim: ts=2 sts=0 sw=2 tw=120 et

from abc import ABC, abstractmethod
from collections import OrderedDict, namedtuple
import getpass
import hashlib
from typing import Callable

from tabulate import tabulate

from deebee.model import (
  ModelClient,
  ModelFavorites,
  ModelFoodType,
  ModelProducts,
  ModelRestaurant,
)

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

class CtxInter(Ctx):
  def __init__(self, mgr, ctx_parent):
    Ctx.__init__(self, mgr)
    self.ctx_parent = ctx_parent
    self.cmds["end"] = Cmd("", self.end)

  def end(self, _):
    self.mgr.ctx = self.ctx_parent

class CtxMain(Ctx):
  def __init__(self, mgr):
    Ctx.__init__(self, mgr)
    self.cmds["login"] = Cmd("<email>", self.login)
    self.cmds["register"] = Cmd("{client <first_name> <last_name> | restaurant <name>} <email> "
      "<street_address> <postal_code> <city> [<phone number>]", self.register)

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

  def register(self, line):
    account_type = line.get_token("account type")
    if account_type is None:
      return
    if account_type not in {"client", "restaurant"}:
      print(f"Error: Invalid account type: {account_type}")
      return
    if account_type == "client":
      first_name = line.get_token("first name")
      if first_name is None:
        return
      last_name = line.get_token("last name")
      if last_name is None:
        return
    else:
      name = line.get_token("name")
      if name is None:
        return
    email = line.get_token("email")
    if email is None:
      return
    street_address = line.get_token("street address")
    if street_address is None:
      return
    postal_code = line.get_token("postal code")
    if postal_code is None:
      return
    city = line.get_token("city")
    if city is None:
      return
    phone_number = line.get_token()
    password = getpass.getpass(prompt="Password: ", stream=None)
    if len(password) == 0:
      print("Error: Password is empty")
      return
    password = hashlib.sha256(password.encode()).digest()
    if account_type == "client":
      result = ModelClient.register(self.mgr.conn, first_name, last_name, email, password, phone_number, street_address,
        postal_code, city)
    else:
      food_types = ModelFoodType.list_food_types(self.mgr.conn)
      print(tabulate(food_types, headers=("ID", "Name"), tablefmt="psql"))
      food_type_id = int(input("Select food type ID: "))
      if food_type_id not in dict(food_types):
        print("Error: Invalid food type ID")
        return
      result = ModelRestaurant.register(self.mgr.conn, name, email, password, phone_number, street_address, postal_code,
        city, food_type_id)
    print("Info: Account has been created" if result else "Error: Could not create account")

class ClientFavorites(CtxInter):
  def __init__(self, mgr, ctx_parent, client_id):
    CtxInter.__init__(self, mgr, ctx_parent)
    self.model = ModelFavorites(mgr.conn, client_id)
    self.cmds["list"] = Cmd("", self.list_favorites)
    self.cmds["add"] = Cmd("<restaurant id>", self.add_fav_entry)
    self.cmds["delete"] = Cmd("<entry id>", self.delete_fav_entry)

  @property
  def name(self):
    return "favorites (client)"

  def list_favorites(self, _):
    header, rows = self.model.list_favorites()
    print(tabulate(rows, header, tablefmt="psql"))

  def add_fav_entry(self, line):
    restaurant_id = line.get_token("restaurant id")
    if restaurant_id is None:
      return
    self.model.add_fav_entry(restaurant_id)

  def delete_fav_entry(self, line):
    entry_id = line.get_token("entry id")
    if entry_id is None:
      return
    self.model.delete_fav_entry(entry_id)

class Client(Ctx):
  def __init__(self, mgr, email):
    Ctx.__init__(self, mgr)
    self.cmds["list"] = Cmd("{restaurants}", self.client_list)
    self.cmds["favorites"] = Cmd("", self.favorites)
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

  def favorites(self, _):
    self.mgr.ctx = ClientFavorites(self.mgr, self, self.model.client_id)

class RestaurantProducts(CtxInter):
  def __init__(self, mgr, ctx_parent, restaurant_id):
    CtxInter.__init__(self, mgr, ctx_parent)
    self.model = ModelProducts(mgr.conn, restaurant_id)
    self.cmds["list"] = Cmd("", self.list_products)
    self.cmds["add"] = Cmd("", self.add_product)
    self.cmds["delete"] = Cmd("<product id>", self.delete_product)

  @property
  def name(self):
    return "products (restaurant)"

  def list_products(self, _):
    header, rows = self.model.list_products()
    print(tabulate(rows, header, tablefmt="psql"))

  def add_product(self, _):
    name = input("Name: ").strip()
    if len(name) == 0:
      print("Error: Empty name")
      return
    description = input("Description: ").strip()
    if len(description) == 0:
      print("Error: Empty description")
      return
    price = float(input("Price: "))
    self.model.add_product(name, description, price)

  def delete_product(self, line):
    product_id = line.get_token("product id")
    if product_id is None:
      return
    self.model.delete_product(int(product_id))

class Restaurant(Ctx):
  def __init__(self, mgr, email):
    Ctx.__init__(self, mgr)
    self.cmds["products"] = Cmd("", self.products)
    self.model = ModelRestaurant.login(mgr.conn, email)

  @property
  def name(self):
    return "restaurant"

  def products(self, _):
    self.mgr.ctx = RestaurantProducts(self.mgr, self, self.model.restaurant_id)

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
