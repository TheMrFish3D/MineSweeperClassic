#!/usr/bin/env python3
"""
Classic Minesweeper Game
Recreates the Windows 3.11 Minesweeper experience for cross-platform use.
"""

from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="minesweeper-classic",
    version="1.0.0",
    author="MineSweeperClassic",
    description="Classic Windows 3.11-style Minesweeper game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "minesweeper=minesweeper.main:main",
        ],
    },
)