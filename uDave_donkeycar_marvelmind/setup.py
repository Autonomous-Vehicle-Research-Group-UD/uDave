import setuptools
from setuptools import setup, Extension
from setuptools.command.install import  install
import os

SRC_DIR = 'src'
SOURCES = ['marvelmind.c', 'plugin.c']
HEADERS = ['marvelmind.h', 'plugin.h']
DONKEYCAR_PATCH_DIRS = ['donkeycar','mycar']
HOME = home_dir = os.environ['HOME']


def get_datafiles(dirs):
    datafiles = []
    for dir in dirs:
        install_path = os.path.join(HOME, dir)
        for path,dirnames,filenames in os.walk(dir):
            data_paths = []
            for fname in filenames:
                data_paths.append(os.path.join(path, fname))
            if data_paths:
                datafiles.append((path,data_paths))
    return datafiles


def expand_sources_path(basepath, sources_list):
    new_list = []
    for source in sources_list:
        new_list.append(os.path.join(basepath, source))
    return new_list


_sources = expand_sources_path(SRC_DIR, SOURCES)
marvelmind_module = Extension('mm_gps', sources=_sources)
module_headers = expand_sources_path(SRC_DIR, HEADERS)

setup(
    name="marvelmind_driver",
    version="0.9.1",
    description="Module for read and parse marvelmind packet stream comes from hedgehog beacon",
    author='Palkovics Dénes, Vágner Máté',
    install_requires=[
        "donkeycar ==3.1.0",
        #'donkeycar@https://github.com/autorope/donkeycar/tarball/3.1.0#egg=donkeycar-3.1.0',
    ],
    dependency_links=[
        "git+https://github.com/autorope/donkeycar@3.1.0#egg=donkeycar-3.1.0",
    ],
    scripts=['bin/patch_mm.sh', 'bin/unpatch_mm.sh'],                                     #These installed under <venv>/bin
    ext_modules=[marvelmind_module],
    data_files=get_datafiles(DONKEYCAR_PATCH_DIRS)
)

