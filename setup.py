import os
from setuptools import setup, find_packages
import sys


tests_require = ["flask", "lxml", "pytest >= 3", "selenium < 3", "werkzeug"]
if sys.version_info < (3, 3):
    tests_require.append("mock")


def read(filename):
    """
    Returns the contents of the given package file.

    Args:
        filename (str): The name of the file to read, relative to the current
            directory.

    Returns:
        str: The contents of the given package file.
    """

    path = os.path.join(os.path.dirname(__file__), filename)

    with open(path) as f:
        return f.read()


def get_version():
    """ str: The package version. """

    global_vars = {}

    # Compile and execute the individual file to prevent
    # the package from being automatically loaded.
    source = read(os.path.join("capybara", "version.py"))
    code = compile(source, "version.py", "exec")
    exec(code, global_vars)

    return global_vars['__version__']


setup(
    name="capybara-py",
    version=get_version(),
    description="Acceptance test framework for web applications",
    long_description=read("README.rst"),
    url="https://github.com/elliterate/capybara.py",
    author="Ian Lesperance",
    author_email="ian@elliterate.com",
    license="MIT",
    keywords="capybara",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing"],
    packages=find_packages(exclude=["tests", "tests.*", "*.tests.*", "*.tests"]),
    install_requires=["xpath-py >= 0.0.4"],
    setup_requires=["pytest-runner"],
    tests_require=tests_require)
