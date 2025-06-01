import os
import sys

from setuptools import Extension, find_packages, setup

name = "sqlidps"

extra_compile_args = []
extra_link_args = []

if sys.platform == "darwin":
    extra_link_args += ["-bundle", "-undefined", "dynamic_lookup"]
    extra_compile_args += ["-fPIC", "-O2", "-Wall"]
elif sys.platform.startswith("linux"):
    extra_compile_args += ["-fPIC", "-O2", "-Wall"]
elif sys.platform.startswith("win"):
    extra_compile_args += ["/O2", "/W3"]

tokenizer_module = Extension(
    name="sqlidps.sql_tokenizer",
    sources=["./sqlidps/lex.yy.c", "./sqlidps/wrapper.c"],
    include_dirs=["./sqlidps"],
    depends=["./sqlidps/wrapper.h"],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c",
)


def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "A simple SQL-injection detector based on ML"


setup(
    name="sqlidps",
    version="1.1.0",
    packages=find_packages(),
    install_requires=["numpy"],
    ext_modules=[tokenizer_module],
    include_package_data=True,
    package_data={
        "sqlidps": ["model.npz", "wrapper.h", "*.c"]  # Include C source files too
    },  # Ensure wrapper.h is included
    zip_safe=False,
    # cmdclass={"build_ext": CustomBuildExt},
    author="Darisi Priyatham, Arjun Manjunath",
    author_email="priyathamdarisi@gmail.com, dev.arjunmnath@gmail.com",
    description="A simple SQL-injection detector based on ML",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DPRIYATHAM/sqlidps/",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
    keywords="sql injection detection security machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/DPRIYATHAM/sqlidps/issues",
        "Source": "https://github.com/DPRIYATHAM/sqlidps/",
    },
)
