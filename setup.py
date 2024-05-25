from setuptools import find_namespace_packages, setup

PACKAGE_NAME_LIB = "24_finance"

print("Building package...")
with open("requirements.txt", "r") as fr:
    requirements = [
        req
        for req in fr.read().splitlines()
        if (not req.startswith("#") and not req.startswith("-e "))
    ]
with open("VERSION", "r") as f:
    version = f.read()
setup(
    name=PACKAGE_NAME_LIB,
    packages=find_namespace_packages(include=["lib", "lib.*", "config", "config.*"]),
    install_requires=requirements,
    version=version,
    description="24 Finance",
    url="https://github.com/artefactory-nl/24Finance.git",
    author="Artefact",
    license="MIT",
)