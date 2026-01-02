#!/usr/bin/env bash
# Unix helper: crea venv, instala deps, crea admin y ejecuta con waitress
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python seed_admin.py
waitress-serve --port=5000 run:app
