from setuptools import setup, find_packages


setup(
    name="dict-treemodel-qt5",
    description="QT5 TreeModel for dict, list and other python types",
    version="0.0.1",
    author="Frederik Schumacher",
    package_dir={
        "": "src"
    },
    packages=[
        "dicttreemodel"
    ],
    install_requires=[
        "PyQt5>=5.12.1"
    ],
    license="UNLICENSE",
    url="https://github.com/fre-sch/dict-treemodel-qt5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
)
