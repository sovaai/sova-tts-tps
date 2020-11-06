from setuptools import setup, find_packages


libname = "TPS"
version = "1.0.0"

setup(
	name=libname,
	version=version,
	author="Virtual Assistants",
	install_requires=[
		"unidecode", "inflect", "nltk"
	],
	packages=find_packages(),
	include_package_data=True,
	description="Text processing for synthesis.",
)