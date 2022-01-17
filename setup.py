import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PACKAGE_DIR = (HERE/"src")

# This call to setup() does all the work
setup(
    name="octopus-energy-client",
    version="0.0.11",
    description="A Python API for retrieving Octopus Energy data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ChristopherJohnston/octopus_energy",
    project_urls={
        "Bug Tracker": "https://github.com/ChristopherJohnston/octopus_energy/issues"
    },
    author="Christopher P Johnston",
    author_email="c.p.johnston@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=["requests", "pytz"],
    python_requires=">=3.6"
)
