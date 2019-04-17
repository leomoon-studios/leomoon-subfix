AppName='LeoMoon SubFix'
#cleanup old build if any
rm -rf "`pwd`/__pycache__"
rm -rf "`pwd`/build"
rm -rf "`pwd`/dist/build"
rm -rf "`pwd`/dist/$AppName.app"
rm -rf "`pwd`/dist/$AppName"
#build python
#/usr/lib/x86_64-linux-gnu/qt5/bin
python3 -m PyInstaller --clean --windowed --onefile --noupx --name "$AppName" --icon=main.ico main.py
#cleanup
rm -rf "`pwd`/dist/$AppName.app/Contents/MacOS/include"
rm -rf "`pwd`/dist/$AppName.app/Contents/MacOS/lib"
rm -rf "`pwd`/dist/$AppName.app/Contents/MacOS/lib2to3"
rm -rf "`pwd`/dist/$AppName.app/Contents/MacOS/PyQt5/Qt/translations"
rm -rf "`pwd`/dist/$AppName.app/Contents/Resources/include"
rm -rf "`pwd`/dist/$AppName.app/Contents/Resources/lib"
rm -rf "`pwd`/dist/$AppName.app/Contents/Resources/lib2to3"
rm -rf "`pwd`/dist/$AppName.app/Contents/Resources/PyQt5/Qt/translations"
cd "`pwd`/dist"
nautilus .