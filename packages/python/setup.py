from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="parse-everything",
    version="1.1.3",
    author="Parse Everything",
    author_email="support@rawmind.app",
    description="Official Python SDK for Parse Everything — Bypass Cloudflare Turnstile, Akamai & DataDome with TLS JA3/JA4 impersonation, GET/POST forwarding & 0-credit failure guarantee.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://parse-everything.com",
    project_urls={
        "Homepage": "https://parse-everything.com",
        "Documentation": "https://parse-everything.com/docs.php",
        "Source Code": "https://github.com/zenkdom/parse-everything",
        "Bug Tracker": "https://github.com/zenkdom/parse-everything/issues",
    },
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "cloudflare-bypass",
        "turnstile-solver",
        "akamai-bypass",
        "datadome",
        "web-scraping-api",
        "ja3-spoofing",
        "ja4-fingerprinting",
        "anti-bot",
        "flaresolverr-alternative",
        "zenrows-alternative",
        "scrapingbee-alternative",
        "crawler",
        "web-extraction"
    ],
    python_requires=">=3.8",
    install_requires=[],
)
