#!/bin/bash -e

if [[ $(uname -s) == MINGW* ]]; then
  python -m venv .venv
  source .venv/Scripts/activate
  pip install -r requirements.txt
  pip install -e .
  alias python='winpty -Xallow-non-tty python.exe'
else
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt
  pip3 install -e .
fi
