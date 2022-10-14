from setuptools import find_packages, setup

# The file describes the project and its files


setup(
    name="flaskr",
    version="1.0.0",
    # Find package directories automatically
    packages=find_packages(),
    # Include other files: static, template directories, schema.sql
    # The other data is as specified in MANIFEST.in
    include_package_data=True,
    install_requires=[
        "flask",
    ],
)
