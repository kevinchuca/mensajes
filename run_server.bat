\
    @echo off
    REM Windows helper: crea venv, instala deps, crea admin y ejecuta con waitress
    python -m venv .venv
    call .venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
    REM Create DB and admin (reads .env for admin creds)
    python seed_admin.py
    REM Run with waitress on port 5000
    call .venv\Scripts\activate
    waitress-serve --port=5000 run:app
