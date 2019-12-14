#-*- coding: utf-8 -*-
import sys
import fileinput

if (len(sys.argv) - 1) != 0:
    version = sys.argv[1]
    versionComma = version.replace('.', ', ')+' ,0'
else:
    print('No version number defined. Exiting...')
    exit()

def _sReplace(filename, search, replace, unixEol=False):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(search, replace), end='')
    if unixEol:
            fileContents = open(filename,"r").read()
            f = open(filename,"w", newline="\n")
            f.write(fileContents)
            f.close()

_sReplace( 'builds/win/version.txt', '1, 0, 0, 0', versionComma, False) #version.txt
_sReplace( 'builds/win/dist/setupgen.iss', '1.0.0', version, False) #setupgen.iss
_sReplace( 'builds/osx/_build.run', '1.0.0', version, True) #_build.run
_sReplace( 'builds/osx/dist/setupgen.pkgproj', '1.0.0', version, True) #setupgen.pkgproj