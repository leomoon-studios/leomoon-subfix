#-*- coding: utf-8 -*-
import sys
# import fileinput
# import codecs
import in_place

if (len(sys.argv) - 1) != 0:
    version = sys.argv[1]
    versionComma = version.replace('.', ', ')+' ,0'
else:
    print('No version number defined. Exiting...')
    exit()

# version = '2.1.3'
# versionComma = version.replace('.', ', ')+' ,0'

def _sReplace(filename, search, replace, unixEol=False):
    # with fileinput.FileInput(filename, openhook=fileinput.hook_encoded("utf-8"), inplace=True) as file:
    #     for line in file:
    #         print(line.replace(search, replace), end='')
    with in_place.InPlace(filename, encoding="utf-8") as file:
        for line in file:
            file.write(line.replace(search, replace))
    if unixEol:
            fileContents = open(filename,"r", encoding="utf-8").read()
            f = open(filename,"w", encoding="utf-8", newline="\n")
            f.write(fileContents)
            f.close()

_sReplace( 'builds/win/main.py', '1.0.0', version, False) #main.py win
_sReplace( 'builds/win/version.txt', '1, 0, 0, 0', versionComma, False) #version.txt
_sReplace( 'builds/win/dist/setupgen.iss', '1.0.0', version, False) #setupgen.iss
_sReplace( 'builds/osx/main.py', '1.0.0', version, False) #main.py osx
_sReplace( 'builds/osx/_build.run', '1.0.0', version, True) #_build.run
_sReplace( 'builds/osx/dist/setupgen.pkgproj', '1.0.0', version, True) #setupgen.pkgproj
_sReplace( 'builds/lin/main.py', '1.0.0', version, False) #main.py win