# vim: ts=2 sts=0 sw=2 tw=100 et

__all__ = ["Model", "dataclass"]

from dataclasses import dataclass

from cx_Oracle import Connection

@dataclass
class Model:
  conn: Connection
