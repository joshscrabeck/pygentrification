
from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='gentrification-indices',
    url='https://github.com/joshscrabeck/gentrification-indices',
    author='Winn Costantini, Josh Scrabeck, and Adam Thompson',
    author_email='josh.scrabeck@temple.edu',
    # Needed to actually package something
    packages=['gentrification-indices'],
    # Needed for dependencies
    install_requires=['io', 'folium','functools','geopandas','math','numpy', 'os', 'pandas', 'requests','tobler', 'urllib', 'warnings', 'zipfile'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='Temple University',
    description='A python module for calculating and visualizing gentrification indices from published academic research',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.txt').read(),
)