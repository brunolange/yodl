"""setup script for yodl
"""

from setuptools import setup

with open('requirements.txt') as handle:
    REQUIREMENTS = handle.readlines()

setup(
    name='yodl',
    version='0.0.1',
    description='Django models from YAML!',
    author='Bruno Lange',
    author_email='blangeram@gmail.com',
    url='https://github.com/brunolange/yodl',
    install_requires=REQUIREMENTS,
    python_requires='>=3',
)
