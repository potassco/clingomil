import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clingomil",
    version="0.0.1",
    author="Jarek Liesen",
    author_email="jliesen@uni-potsdam.de",
    description="Meta-interpretive learning using clingo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitup.uni-potsdam.de/jliesen/clingomil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=["pyswip"],
    dependency_links=[
        # "https://gitup.uni-potsdam.de/jliesen/pyswip/repository/archive.tar.gz#egg=pyswip-0.2.7",
        # Here, we are using this version of pyswip, as it enables unification
        # with strings and lists
        "https://github.com/tkchouaki/pyswip/tarball/master#egg=pyswip-0.2.7",
    ],
)
