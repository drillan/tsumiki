from setuptools import setup, find_packages


def read_file(filename):
    with open(filename, "r", encoding="utf8") as f:
        return f.read()


setup(
    name="tsumiki",
    version="0.0.2",
    url="https://github.com/drillan/tsumiki",
    author="driller",
    description="tsumiki is a markup language to process multiple columns.",
    long_description=read_file('README.rst'),
    python_requires=">=3.6",
    install_requires=["markdown", "py-gfm", "jinja2", "jinja2schema", "Click"],
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
    entry_points="""
        [console_scripts]
        tsumiki=tsumiki.cmd:tsumiki
    """,
)
