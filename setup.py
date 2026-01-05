#!/usr/bin/env python3
"""
Setup script for TextTokenizationEngine package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="santok",
    version="1.0.0",
    author="Santosh Chavala",
    author_email="chavalasantosh@example.com",
    description="SanTOK - A comprehensive text tokenization system with mathematical analysis and statistical features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chavalasantosh/SanTOK",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - pure Python
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "santok=santok.cli:main",
        ],
    },
)
