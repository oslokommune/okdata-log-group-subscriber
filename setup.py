from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="okdata-log-group-subscriber",
    version="0.1.0",
    author="Origo Dataplattform",
    author_email="dataplattform@oslo.kommune.no",
    description="Auto-subscribe to CloudWatch Log Groups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-log-group-subscriber",
    packages=find_packages(),
    install_requires=[
        "aws-xray-sdk",
        "boto3",
        # XXX: Don't upgrade this package to 7.14 or later, since it doesn't
        # work with AWS' OpenSearch Service.
        "elasticsearch<7.14",
        "okdata-aws",
        "requests-aws4auth",
    ],
)
