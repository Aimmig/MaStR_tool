from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="mastr_osm_utils",
    version="0.0.1",
    description="Download, filter MaStRData and compare to existing osm data",
    packages=find_packages(),
    install_requires=requirements
)
