from setuptools import setup

setup(
    name="circuitpython-ampule",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="CircuitPython framework for building simple web applications",
    long_description="CircuitPython framework for building simple web applications",
    long_description_content_type="text/markdown",
    url="https://github.com/deckerego/ampule",
    author="DeckerEgo",
    author_email="john@deckerego.net",
    py_modules=["ampule"],
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
)
