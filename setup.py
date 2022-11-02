import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='2dwavesim',
    version='1.0.0',
    author='Cooper Hatfield',
    author_email='cooperhatfield@yahoo.ca',
    description='Simulate waves on 2D surfaces with arbitrary shape/size!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cooperhatfield/2dwavesim',
    project_urls = {
        "Bug Tracker": "https://github.com/cooperhatfield/2dwavesim/issues"
    },
    license='',
    packages=['2dwavesim'],
    install_requires=['numpy', 'tqdm'],
)