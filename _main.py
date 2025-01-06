#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# NSMBU RANDOMIZER
# This was a modified version of the SarcTool by AboodXD, running NinTyler's randomizer to jumble the files, then modifying the file in the level to not crash.


################################################################

import os
import sys
import time
import re
try:
    import SarcLib

except ImportError:
    print("SarcLib is not installed!")
    ans = input("Do you want to install it now? (y/n)\t")
    if ans.lower() == 'y':
        import pip
        pip.main(['install', 'SarcLib==0.3'])
        del pip

        import SarcLib

    else:
        sys.exit(1)

try:
    import libyaz0

except ImportError:
    print("libyaz0 is not installed!")
    ans = input("Do you want to install it now? (y/n)\t")
    if ans.lower() == 'y':
        import pip
        pip.main(['install', 'libyaz0==0.5'])
        del pip

        import libyaz0

    else:
        sys.exit(1)



def extract(file):
    """
    Extrct the given archive
    """
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(file)[0]
    ext = SarcLib.guessFileExt(inb)

    if ext != ".sarc":
        with open(''.join([name, ext]), "wb") as out:
            out.write(inb)

    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(os.path.dirname(file), name)
        if not os.path.isdir(root):
            os.mkdir(root)

        files = []

        def getAbsPath(folder, path):
            nonlocal root
            nonlocal files

            for checkObj in folder.contents:
                if isinstance(checkObj, SarcLib.File):
                    files.append(["/".join([path, checkObj.name]), checkObj.data])

                else:
                    path_ = os.path.join(root, "/".join([path, checkObj.name]))
                    if not os.path.isdir(path_):
                        os.mkdir(path_)

                    getAbsPath(checkObj, "/".join([path, checkObj.name]))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])

            else:
                path = os.path.join(root, checkObj.name)
                if not os.path.isdir(path):
                    os.mkdir(path)

                getAbsPath(checkObj, checkObj.name)

        for file, fileData in files:
            # print(file)
            with open(os.path.join(root, file), "wb") as out:
                out.write(fileData)


def pack(root, level, outname = False): # endianness, 
    """
    Pack the files and folders in the root folder.
    """

    if "\\" in root:
        root = "/".join(root.split("\\"))

    if root[-1] == "/":
        root = root[:-1]

    arc = SarcLib.SARC_Archive() # endianness=endianness
    lenroot = len(root.split("/"))

    for path, dirs, files in os.walk(root):
        if "\\" in path:
            path = "/".join(path.split("\\"))

        lenpath = len(path.split("/"))

        if lenpath == lenroot:
            path = ""

        else:
            path = "/".join(path.split("/")[lenroot - lenpath:])

        for file in files:
            if path:
                filename = ''.join([path, "/", file])

            else:
                filename = file

            # print(filename)

            fullname = ''.join([root, "/", filename])

            i = 0
            for folder in filename.split("/")[:-1]:
                if not i:
                    exec("folder%i = SarcLib.Folder(folder + '/'); arc.addFolder(folder%i)".replace('%i', str(i)))

                else:
                    exec("folder%i = SarcLib.Folder(folder + '/'); folder%m.addFolder(folder%i)".replace('%i', str(i)).replace('%m', str(i - 1)))

                i += 1

            with open(fullname, "rb") as f:
                inb = f.read()

            hasFilename = True
            if file[:5] == "hash_":
                hasFilename = False

            if not i:
                arc.addFile(SarcLib.File(file, inb, hasFilename))

            else:
                exec("folder%m.addFile(SarcLib.File(file, inb, hasFilename))".replace('%m', str(i - 1)))

    data, maxAlignment = arc.save()

    if level != -1:
        outData = libyaz0.compress(data, maxAlignment, level)
        del data

        if not outname:
            outname = ''.join([root, ".szs"])

    else:
        outData = data
        if not outname:
            outname = ''.join([root, ".sarc"])

    with open(outname, "wb+") as output:
        output.write(outData)

os.system("cmd /c SortingFile.bat")

os.chdir("CopyOfFiles")
for file in os.listdir():
    extract(file)
    name = file.replace(".szs", "")
    os.remove(file)
    os.chdir(name)
    filtered_files = [name for name in os.listdir() if re.findall(r'.*-*$', name)]
    # print(filtered_files)
    os.rename(filtered_files[0], name)
    os.chdir("..")
    pack(root=name, level=1)
    os.system(f"del /F /Q {name}")
    print(f"Compressed {name}")
