from setuptools import setup, find_packages

setup(
    name="multiformat-validator",
    version="3.0.0",
    packages=find_packages(),
    install_requires=["colorama>=0.4.6"],
    extras_require={
        "yaml": ["pyyaml>=6.0"],
    },
    entry_points={
        "console_scripts": [
            "check-cli=multiformat_validator.cli:main",
        ],
    },
    python_requires=">=3.12",
)
