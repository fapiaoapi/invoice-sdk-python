from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tax-invoice",
    version="1.0.9",
    author="yuejianghe",
    author_email="yuejianghe@qq.com",
    description="发票SDK Python 电子发票/数电发票/全电发票/数电票/开票",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fapiaoapi/invoice-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)