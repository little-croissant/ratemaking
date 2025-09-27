from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="credibility-tools",
    version="0.1.0",
    author="Aria Team",
    description="A Python library for actuarial credibility calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # credibility_tools.py only uses standard library
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "numpy>=1.20.0",
            "pandas>=1.3.0",
            "pyperclip>=1.8.0",
            "pyautogui>=0.9.0",
            "watchdog>=2.0.0",
        ],
    },
)
