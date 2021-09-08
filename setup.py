from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="circuitpython-ampule",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="CircuitPython framework for building simple web applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deckerego/ampule",
    author="DeckerEgo",
    author_email="john@deckerego.net",
    install_requires=[],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="adafruit circuitpython micropython web server webserver app webapp framework http https bottle",
    py_modules=["ampule"],
)
