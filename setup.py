import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nodejsscan_results_omitter",
    version="0.0.1",
    author="Financial-Times/cybersec",
    author_email="cyber.security@ft.com",
    description="A module to omit results from the NodeJsScan output file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Financial-Times/nodejsscan-results-omitter/",
    packages=["nodejsscan_results_omitter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "nodejsscan-results-omitter=nodejsscan_results_omitter.__main__:main"
        ]
    },
)
