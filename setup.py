from setuptools import find_packages, setup

setup(
    name="sqlidps",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "joblib", "scikit-learn", "pandas", "numpy", "setuptools"
        ],
    include_package_data=True,  
    package_data={
        "sqlidps": [    
            "inference.py",
            "model.pkl",
            "sql_tokenizer.so",
        ],
    },
    author="Darisi Priyatham, Arjun Manjunath",
    author_email="priyathamdarisi@gmail.com, dev.arjunmnath@gmail.com",
    description="A Simple SQL injection detection and prevention package using ML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DPRIYATHAM/sqlidps/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)