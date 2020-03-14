#!/bin/bash
if [ ! -d ".venv" ]
then
    python3 -m venv .venv
    .venv/bin/python3 -m pip install beautifulsoup4
fi
.venv/bin/python3 main.py