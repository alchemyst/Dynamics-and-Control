import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# See https://packaging.python.org/guides/single-sourcing-package-version/
exec(open("tbcontrol/version.py").read())

setuptools.setup(
    name="tbcontrol",
    version=__version__,
    author="Carl Sandrock",
    author_email="carl.sandrock@gmail.com",
    description="Textbook Control Problem package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alchemyst/Dynamics-and-Control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
    ],
    python_requires=">=3.5",
    install_requires=["numpy", "scipy", "tqdm", "packaging"],
)
