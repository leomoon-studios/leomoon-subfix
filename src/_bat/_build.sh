AppName='LeoMoon SubFix'
AppNameLc=$(echo ${AppName,,} | tr ' ' '-')
# cleanup old build if any
rm -rf "`pwd`/__pycache__"
rm -rf "`pwd`/build"
rm -rf "`pwd`/dist/build"
rm -rf "`pwd`/dist/$AppName"
# build python
python3.8 -m PyInstaller --clean --windowed --onedir --noupx --name "$AppName" --icon=main.ico main.py
rm -rf "`pwd`/dist/$AppName/PyQt5/Qt/translations"
# deb packaging
cd "`pwd`/dist"
mkdir "deb-package/opt/"
mkdir "deb-package/usr/bin/"
ln -s "/opt/$AppNameLc/$AppName" "deb-package/usr/bin/$AppNameLc"
chmod -R 755 deb-package/
cp main.png "$AppName/"
mv "$AppName" "deb-package/opt/$AppNameLc/"
dpkg-deb --build ./deb-package
mv deb-package.deb "${AppNameLc}_lin.deb"
# nautilus .
