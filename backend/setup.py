from setuptools import setup, find_packages

setup(
    name="recycling_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn"
    ],
)
