#!/usr/bin/env python3
"""
Setup script for SOMA (formerly SOMA) package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="soma",
    version="1.0.0",
    author="Santosh Chavala",
    author_email="chavalasantosh@gmail.com",
    description="SOMA - Advanced AI Tokenization & Intelligence Framework (formerly SOMA)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chavalasantosh/SanVerse",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies
    ],
    entry_points={
        "console_scripts": [
            "soma=soma_cli:main",
        ],
    },
)
