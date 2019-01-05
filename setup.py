# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = '1.1.0'

setup(
    name="first_blood",
    version=__version__,
    packages=find_packages(exclude=["tests.*", "tests", "docs", "scripts", 'font', "web_console", "website"]),
    description="first_blood description",
    long_description="first_blood long description",
    author="no_one",
    author_email="no_one@xxx.com",
    include_package_data=True,
    zip_safe=False,
    license="Proprietary",
    keywords=("first", "egg"),
    platforms="any",
    install_requires=['Flask', 'Flask-SQLAlchemy', 'requests', 'redis', 'pyyaml', 'pycrypto'],
    entry_points={},
)
