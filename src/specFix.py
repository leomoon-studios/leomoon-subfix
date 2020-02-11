import fileinput
import sys

if (len(sys.argv) - 1) != 0:
    SPECFILE = sys.argv[1]
else:
    print('[!] Please define spec file name to edit.')
    exit()

for line in fileinput.input(SPECFILE, inplace=True):
    if line.strip() == 'pyz = PYZ(a.pure, a.zipped_data,':
        sys.stdout.write(
            "a.binaries = a.binaries - TOC([('d3dcompiler_47.dll', None, None),('opengl32sw.dll', None, None)])\n"
            "pyz = PYZ(a.pure, a.zipped_data,\n"
        )
    else:
        sys.stdout.write(line)