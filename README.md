# Bridge Analyzer

This is the fun project involving ~~procedurally generating~~ (WIP) trusses as a bridge which are then verified with finite-element analysis.

## Installation

```bash
python3 -m pip install -r requirements.txt
```

It is recommended to initiate a Python virtual environment (`venv`) in this
top-level directory so that you can keep the dependency of this project
separate from your system Python modules. To create one, simply change your
working directory here, then

```bash
python3 -m venv .
```

## Usage

Two versions currently exist (merging in progress):
to run Maximo/Artem's version, do `python main.py`;
to run Stephen's version, do `./cooler.py` (or `.\cooler.py` on Windows)
when using a Python virtual environment located in this directory.

PS use Python <3.8 (not including) if you can in case the installation script
for older versions of `matplotlib` uses deprecated and removed functions.
