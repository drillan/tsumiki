from setuptools import setup, find_packages


setup(
    name="tsumiki",
    version="0.0.1a1",
    url="https://github.com/drillan/tsumiki",
    author="driller",
    description="Jupyter(IPython) cell magic for display multiple columns [Markdown/HTML].",
    python_requires=">=3.6",
    install_requires=["markdown", "py-gfm", "jinja2"],
    license="MIT",
    # py_modules=["tsumiki"],
    packages=find_packages(),
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
