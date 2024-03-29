#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["loguru==0.5.3", "requests==2.25.1"]

test_requirements = [
    "pip",
    "wheel",
    "bump2version==1.0.1",
    "watchdog==2.1.3",
    "flake8==3.9.2",
    "tox==3.23.1",
    "coverage==5.5",
    "Sphinx==4.0.2",
    "twine==3.4.1",
    "loguru==0.5.3",
    "requests==2.25.1",
]

setup(
    author="Paul Armstrong",
    author_email='paul.armstrong211@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python wrapper for interacting with the tv db api",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tv_db_api',
    name='tv_db_api',
    packages=find_packages(include=['tv_db_api', 'tv_db_api.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/paul-armstrong-dev/tv_db_api',
    version='0.1.3',
    zip_safe=False,
)
