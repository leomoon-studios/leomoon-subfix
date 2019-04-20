AppName='LeoMoon SubFix'
#cleanup old build if any
rm -rf "`pwd`/__pycache__"
rm -rf "`pwd`/build"
rm -rf "`pwd`/dist/build"
rm -rf "`pwd`/dist/$AppName"
#build python
#/usr/lib/x86_64-linux-gnu/qt5/bin
python3 -m PyInstaller --clean --windowed --onefile --noupx --name "$AppName" --icon=main.ico main.py
#open folder
cd "`pwd`/dist"
nautilus .