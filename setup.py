from setuptools import setup, find_packages

setup(
    name="seek_core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0",
        "openai>=1.0.0",
        "pytest>=7.0.0"
    ],
    description="Seek's core logic for roadmap generation and adaptive learning",
    author="Petimus",
)
