import fileinput
import sys

if (len(sys.argv) - 1) != 0:
    SPECFILE = sys.argv[1]
else:
    print('[!] Please define spec file name to edit.')
    exit()

for line in fileinput.input(SPECFILE, inplace=True):
    if line.strip() == 'exe = EXE(pyz,':
        sys.stdout.write(
            "a.binaries = a.binaries - TOC(["
            "('d3dcompiler_47.dll', None, None),"
            "('libEGL.dll', None, None),"
            "('libGLESv2.dll', None, None),"
            "('opengl32sw.dll', None, None),"
            "('Qt5DBus.dll', None, None),"
            "('Qt5Qml.dll', None, None),"
            "('Qt5QmlModels.dll', None, None),"
            "('Qt5Quick.dll', None, None),"
            "('Qt5WebSockets.dll', None, None)"
            "])\n"
            "exe = EXE(pyz,\n"
        )
    else:
        sys.stdout.write(line)