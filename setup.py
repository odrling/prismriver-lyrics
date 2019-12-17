#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import re
import sys

from setuptools import find_packages, setup


def get_metadata(metadata_file):
    with open(metadata_file) as stream:
        text = stream.read()

        ex = r"__(\w*?)__\s*?=\s*?[\"\']([^\"\']*)"
        items = re.findall(ex, text)
        metadata = {key: value for key, value in items}

        metadata['keywords'] = metadata.get('keywords', '').split(', ')

        ex = r'"{3}[^\w]*(?P<name>[^\s]*)[^\w]+(?P<description>.*)'
        match = re.search(ex, text)

        metadata.update(match.groupdict())

    return metadata


ex = r"# ([^\s:]+).*\n([^#]+)"
requirements_prog = re.compile(ex)


def get_requirements(requirements):
    with open(requirements) as stream:
        matches = requirements_prog.findall(stream.read())
        requires = {key: value.strip().splitlines()
                    for key, value in matches}

    return requires


def main():
    dirname = os.path.dirname(inspect.getfile(inspect.currentframe()))

    # get metadata and keywords from peony/__init__.py
    kwargs = get_metadata(os.path.join(dirname, 'prismriver', '__init__.py'))

    # get requirements from requirements.txt
    kwargs.update(get_requirements(os.path.join(dirname, 'requirements.txt')))

    # get extras requirements from extras_require.txt
    extras = os.path.join(dirname, 'extras_require.txt')
    extras_require = get_requirements(extras)

    # get long description from README.md
    with open('README.md') as stream:
        long_description = stream.read()

    setup(long_description=long_description,
          packages=find_packages(include=["prismriver*"]),
          extras_require=extras_require,
          python_requires='>=3.3',  # I'll trust the README
          **kwargs)


if __name__ == '__main__':
    main()
