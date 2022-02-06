#!/usr/bin/env python
import re

from pathlib import Path

from setuptools import setup


root_dir = Path(__file__).resolve().parent

script_file = root_dir / "gol.py"
content = script_file.read_text(encoding="utf-8")
author = re.search(r"__author__ = \"([\w\s]+)\"", content).group(1)
version = re.search(r"__version__ = \"(\d\.\d\.\d)\"", content).group(1)

readme = (root_dir / "README.md").read_text(encoding="utf-8")

dev_dependencies = (
    (root_dir / "requirements-dev.txt").read_text(encoding="utf-8").splitlines()
)

setup(
    name="gol",
    version=version,
    description="Conway's Game of Life as a TUI.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author=author,
    maintainer=author,
    license="MIT",
    py_modules=["gol"],
    entry_points={"console_scripts": "gol=gol:main"},
    python_requires=">=3.7",
    extras_require={"dev": dev_dependencies},
    setup_requires=["setuptools", "wheel"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
