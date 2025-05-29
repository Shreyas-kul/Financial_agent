from setuptools import setup, find_packages

setup(
    name="financial_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "python-dotenv>=1.0.1",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "yfinance>=0.2.36",
        "requests>=2.31.0",
        "crewai>=0.5.0",
        "openai>=1.12.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "python-multipart>=0.0.9",
        "pytz>=2024.1",
        "beautifulsoup4>=4.12.3",
        "fastapi>=0.109.1",
        "uvicorn>=0.27.0",
        "httpx>=0.26.0",
        "aiohttp>=3.9.3",
    ],
) 