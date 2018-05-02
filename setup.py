from setuptools import setup

try:
    import pathlib
except ImportError as e:
    raise ImportError("This Python is old. `pathlib` is required.")

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.read().split()

setup(name="gsync",
      version="alpha",
      author="moskomule",
      author_email="hataya@nlab.jp",
      package=["gsync"],
      url="https://github.com/moskomule/gsync",
      description="PyDrive wrapper",
      long_description=readme,
      license="BSD",
      install_requires=requirements,
      entry_points={"console_scripts": ["gsync=gsync.commandline:main"]}
      )
