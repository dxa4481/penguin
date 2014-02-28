#!/bin/env python
# -*- coding: utf8 -*-

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup




version = "0.0.1"

setup(
    name="Penguin",
    version=version,
    description="A tool sharing app",
    keywords="",
    author="NPMC",
    author_email="dxa4481@rit.edu",
    url="control.se.rit.edu/home/teams/261/s261-08d/svn/trunk",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Django",
    ],
    #TODO: Deal with entry_points
    #entry_points="""
    #[console_scripts]
    #pythong = pythong.util:parse_args
    #"""
)
