from setuptools import setup, find_packages

setup(
    name="deepseek-inference-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "transformers",
        "torch",
        "pytest",
        "httpx",
        "pytest-asyncio",
    ],
) 