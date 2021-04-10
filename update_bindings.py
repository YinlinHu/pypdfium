#! /usr/bin/env python3

# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2021 Manuel Geißer <geisserml@gmail.com>

SPDX-License-Identifier: MIT
""" 

import tarfile
import zipfile
import subprocess
import os
import glob
import shutil
from urllib import request

# determine current directory for relative paths
thisdirectory = os.path.dirname(os.path.realpath(__file__)) + '/'

# install/update ctypesgen
subprocess.run("python3 -m pip install -U ctypesgen", shell=True)

# extract the latest tag needed to determine the URL
latest_tag = subprocess.run(["git ls-remote https://github.com/bblanchon/pdfium-binaries.git |grep -ohP 'chromium/\d+' |tail -n1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
latest_tag = latest_tag.stdout.decode('UTF-8')[:-1].split('/')[1]
print(latest_tag)

# update version file
with open(thisdirectory+'pypdfium/pdfium_version.txt', 'w') as f:
    f.write('chromium/'+latest_tag)

# craft release url
base_url = "https://github.com/bblanchon/pdfium-binaries/releases/download/chromium%2F" + latest_tag + '/'
print(base_url)

# files to download
filenames = {
    'linux' : 'pdfium-linux.tgz',
    'darwin' : 'pdfium-darwin-x64.tgz',
    'win32' : 'pdfium-windows-x64.zip',
}

# initialise dict to fill in the paths of the downloaded files
files = dict()

# download tarballs & zipfile and update the paths dictionary
for platform, file in filenames.items():
    download_url = base_url + file
    target_path = thisdirectory+file
    print(download_url, target_path)
    request.urlretrieve(download_url, target_path)
    files.update({platform : target_path})

print(files)


# functions to extract single files without their parent directories

def tar_flatextract(member):
    for info in archive.getmembers():
        if info.name.endswith(member):
            if info.name[-1] == '/':
                continue
            info.name = os.path.basename(info.name)
            archive.extract(info, './pypdfium')

def zip_flatextract(member):
    for info in archive.infolist():
        if info.filename.endswith(member):
            if info.filename[-1] == '/':
                continue
            info.filename = os.path.basename(info.filename)
            archive.extract(info, './pypdfium')


# extract the archives

for platform, file in files.items():
    
    # open the archive
    if file.endswith('.tgz'):
        archive = tarfile.open(file, 'r')
    elif file.endswith('.zip'):
        archive = zipfile.ZipFile(file, 'r')
    
    # Linux binary extraction
    # special because we will be using the Linux archive for ctypesgen
    if platform == 'linux':
        archive.extractall('./linux_tar')
        shutil.copyfile('./linux_tar/lib/libpdfium.so', './pypdfium/pdfium')
    
    # macOS and Windows binary extraction
    elif platform == 'darwin':
        tar_flatextract('lib/libpdfium.dylib')
    elif platform == 'win32':
        zip_flatextract('x64/bin/pdfium.dll')
    
    # close the archive and delete it
    archive.close()
    os.remove(file)


# finally, call ctypesgen
ctypesgen_command = f"ctypesgen -lpdfium -L {thisdirectory}linux_tar/lib {thisdirectory}linux_tar/include/*.h -o pypdfium/pypdfium.py"
print(ctypesgen_command)
subprocess.run([ctypesgen_command], shell=True)


# delete the extracted Linux pdfium binary + headers
shutil.rmtree(thisdirectory+'linux_tar/')


# build the wheel
wheel_command = 'python3 setup.py bdist_wheel'
print(wheel_command)
subprocess.run([wheel_command], shell=True)


# install wheel locally

# get all files in the dist/ directory
builddir_files = glob.glob(f'{thisdirectory}dist/*')

# take the latest one
wheel = max(builddir_files, key=os.path.getctime)
print(wheel)

# craft install command
install_command = f'python3 -m pip install -U ' + wheel
print(install_command)

# run it
subprocess.run(install_command, shell=True)
