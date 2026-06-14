#!/usr/bin/env python3

import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: denv.py <typefile> <run-setting : optional>")
    exit()

arg = sys.argv

if arg[1] == "-v" or arg[1] == "-version":
    print("DEnv version 1.0.0\nCopyright (C) 2026 Alex Pesta")
    exit()

elif arg[1] == "-c":
    if len(arg) <= 2:
        subprocess.run(["bash", "scripts/c/c-default.sh"])
    else:
        if len(arg) >= 3:
            if arg[2] == "-C-All":
                subprocess.run(["bash", "scripts/c/c-all.sh"])

elif arg[1] == "-cpp" or arg[1] == "-c++":
    if len(arg) <= 2:
        subprocess.run(["bash", "scripts/cpp/cpp-default.sh"])
    else:
        if len(arg) >= 3:
            if arg[2] == "-CPP-All":
                subprocess.run(["bash", "scripts/cpp/cpp-all.sh"])

elif arg[1] == "-py" or arg[1] == "-python":
    if len(arg) <= 2:
        subprocess.run(["bash", "scripts/python/python-default.sh"])
    else:
        if len(arg) >= 3:
            if arg[2] == "-no-pycache":
                subprocess.run(["bash", "scripts/python/python-no-pycache.sh"])
