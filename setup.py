#!/usr/bin/python3

from setuptools import setup
setup(
    name="redpaper",
    version="0.1.0",
    install_requires=['docutils>=0.3', 'praw>=6.2.0'],

    # metadata to display on PyPI
    author="Teddy Okello",
    author_email="keystroke3@gmail.com",
    description="A program to download and change desktop wallpapers",
    keywords="change wallpaper reddit in linux desktop gnome kde xfce budgie",
    url="https://github.com/keystroke3/redpaper",   # project home page, if any
    package_dir={'': 'src'},
    project_urls={
        "Bug Tracker": "https://github.com/keystroke3/redpaper/issues",
        "Documentation": "https://github.com/keystroke3/redpaper/wiki",
        "Source Code": "https://github.com/keystroke3/redpaper",
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ]
)
