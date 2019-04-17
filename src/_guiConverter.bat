::set where pyuic is located
::	pyuic4 = "c:\Python27\Lib\site-packages\PyQt4\pyuic4.bat"
::	pyuic5 = "C:\Python35-32\Lib\site-packages\PyQt5\pyuic5.bat"

SET pyuic="C:\Python\Scripts\pyuic5.exe"
SET pyrcc="C:\Python\Scripts\pyrcc5.exe"

cd gui
del *.py

if exist resources.qrc ( %pyrcc% resources.qrc -o ..\resources_rc.py )

for %%f in (*.ui) do (
	echo "%%~nf.ui"
	%pyuic% -d "%%~nf.ui" -o "%%~nf.py"
)