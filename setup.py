import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sharp_darwin",
    version="1.3.7",
    author="Robert Sigler",
    author_email="sigler@improvisedscience.org",
    description="Spotify Playlist Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmrfslashbin/sharp-darwin",
    packages=["sharp_darwin"],
    install_requires=[
        "spotipy>=2.10",
        "python-dotenv>=0.12",
        "argcomplete>=1.11"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points = {
        "console_scripts": [
            "sharp-darwin=sharp_darwin.sharp_darwin_cli:main"
        ]
    }
)
