import os
import subprocess
import sys

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

name = "sqlidps"

extra_compile_args = []
extra_link_args = []

if sys.platform == "darwin":
    extra_link_args += ["-bundle", "-undefined", "dynamic_lookup"]
    extra_compile_args += ["-fPIC", "-O2", "-Wall"]
elif sys.platform.startswith("linux"):
    extra_compile_args += ["-fPIC", "-O2", "-Wall"]

tokenizer_module = Extension(
    name="sqlidps.sql_tokenizer",
    sources=["./sqlidps/lex.yy.c", "./sqlidps/wrapper.c"],
    include_dirs=["./sqlidps"],
    headers=["./sqlidps/wrapper.h"],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c",
)

setup(
    name="sqlidps",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["numpy"],
    ext_modules=[tokenizer_module],
    include_package_data=True,
    package_data={
        "sqlidps": ["model.npz", "wrapper.h"]
    },  # Ensure wrapper.h is included
    # cmdclass={"build_ext": CustomBuildExt},
    author="",
    author_email="your.email@example.com",
    description="A simple SQL-injection detector based on ML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DPRIYATHAM/sqli-dps/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
