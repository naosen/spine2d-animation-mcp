from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="spine2d-animation-mcp",
    version="0.1.0",
    author="",
    author_email="",
    description="MCP server for generating SPINE2D animations from PSD files using natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spine2d-animation-mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "spine2d-mcp=src.main:main",
        ],
    },
)