"""
SPDX-FileCopyrightText: 2021 Manuel Geißer <geisserml@gmail.com>

SPDX-License-Identifier: MIT
""" 

import tarfile
import zipfile
import subprocess
import os
import shutil
from urllib import request

"""
TODO
install/update ctypesgen
download latest binaries DONE
extract required files DONE
call ctypesgen on extracted linux tar
commit
build wheel
"""

# determine current directory for relative paths
thisdirectory = os.path.dirname(os.path.realpath(__file__)) + '/'

# install/update ctypesgen
subprocess.run("python3 -m pip install -U ctypesgen", shell=True)

# extract the latest tag needed to determine the URL
latest_tag = subprocess.run(["git ls-remote https://github.com/bblanchon/pdfium-binaries.git |grep -ohP 'chromium/\d+' |tail -n1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
latest_tag = latest_tag.stdout.decode('UTF-8')[:-1].split('/')[1]
print(latest_tag)

base_url = "https://github.com/bblanchon/pdfium-binaries/releases/download/chromium%2F" + latest_tag + '/'
print(base_url)

filenames = {
    'linux' : 'pdfium-linux.tgz',
    'darwin' : 'pdfium-darwin-x64.tgz',
    'win32' : 'pdfium-windows-x64.zip',
}

files = dict()

for platform, file in filenames.items():
    download_url = base_url + file
    target_path = thisdirectory+file
    print(download_url, target_path)
    request.urlretrieve(download_url, target_path)
    files.update({platform : target_path})

print(files)


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


for platform, file in files.items():
    
    if file.endswith('.tgz'):
        archive = tarfile.open(file, 'r')
    elif file.endswith('.zip'):
        archive = zipfile.ZipFile(file, 'r')
    
    if platform == 'linux':
        archive.extractall('./linux_tar')
        shutil.copyfile('./linux_tar/lib/libpdfium.so', './pypdfium/libpdfium')
    elif platform == 'darwin':
        tar_flatextract('lib/libpdfium.dylib')
    elif platform == 'win32':
        zip_flatextract('x64/bin/pdfium.dll')
    
    archive.close()
    os.remove(file)

subprocess.run([f"ctypesgen -lpdfium -L {thisdirectory}/linux_tar/lib {thisdirectory}/linux_tar/include/*.h -o pypdfium/pypdfium.py"], shell=True)
shutil.rmtree(thisdirectory+'linux_tar/')
