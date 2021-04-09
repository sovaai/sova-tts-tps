from setuptools import setup, find_packages


libname = "TPS"
version = "1.2.0"

setup(
	name=libname,
	version=version,
	author="Virtual Assistants",
	install_requires=[
		"unidecode", "inflect", "nltk", "tqdm", "loguru"
	],
	packages=find_packages(),
	description="Text processing for synthesis.",
)