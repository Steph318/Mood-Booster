from pathlib import Path
import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="Mood-Booster",
    version="0.0.1",
    author="Damaris",
    author_email="dsndjebayi@aimsammi.org",
    description="Mood Booster app help you to chat using audio with AI model, to help you change your mood",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steph318",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=0.63",
    ],
)