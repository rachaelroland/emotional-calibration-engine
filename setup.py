from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="emotional-calibration-engine",
    version="0.1.0",
    author="Rachael Roland",
    author_email="",
    description="A scientifically-grounded framework for emotional calibration and self-understanding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rachaelroland/emotional_calibration_engine",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ece=emotional_calibration_engine.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "emotional_calibration_engine": ["configs/*.yaml", "protocols/*.yaml", "data/*.json"],
    },
)