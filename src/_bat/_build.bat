::pre cleanup
SET AppName=LeoMoon SubFix
rmdir "%cd%\dist\build\" /s/q
rmdir "%cd%\dist\%AppName%\" /s/q
rmdir "%cd%\__pycache__\" /s/q
::define multiple paths using semicolon
::--paths C:\Python\Lib\site-packages\PyQt5\Qt\bin
C:\Python\python -m PyInstaller --add-binary *.dll;. --clean --windowed --onefile --noupx --name "%AppName%" --version-file=version.txt --icon=main.ico main.py
::cleanup
rmdir "%cd%\dist\%AppName%\PyQt5\Qt\bin\" /s/q
rmdir "%cd%\dist\%AppName%\PyQt5\Qt\translations\" /s/q
rmdir "%cd%\dist\%AppName%\adodbapi\" /s/q
rmdir "%cd%\dist\%AppName%\Demos\" /s/q
rmdir "%cd%\dist\%AppName%\Include\" /s/q
rmdir "%cd%\dist\%AppName%\isapi\" /s/q
rmdir "%cd%\dist\%AppName%\lib2to3\" /s/q
rmdir "%cd%\dist\%AppName%\libs\" /s/q
rmdir "%cd%\dist\%AppName%\pywin\" /s/q
rmdir "%cd%\dist\%AppName%\test\" /s/q
rmdir "%cd%\dist\%AppName%\win32com\" /s/q
rmdir "%cd%\dist\%AppName%\win32comext\" /s/q
rmdir "%cd%\dist\build\" /s/q
del "%cd%\dist\%AppName%\license.txt"
del "%cd%\dist\%AppName%\pythonservice.exe"
del "%cd%\dist\%AppName%\Pythonwin.exe"
del "%cd%\dist\%AppName%\PyWin32.chm"
del "%cd%\dist\%AppName%\pywin32.pth"
del "%cd%\dist\%AppName%\pywin32.version.txt"
del "%cd%\dist\%AppName%\pywin32-221-py3.6.egg-info"
del "%cd%\dist\%AppName%\_ssl.pyd"
del "%cd%\dist\%AppName%\_hashlib.pyd"
del "%cd%\dist\%AppName%\mfc140u.dll"
::prepare
if not exist "%cd%\dist\%AppName%\" mkdir "%cd%\dist\%AppName%\"
if exist "%cd%\dist\%AppName%.exe" move "%cd%\dist\%AppName%.exe" "%cd%\dist\%AppName%\"
::sign app
SET sign=%cd%\signtool\signtool.exe
SET pfx=%cd%\signtool\cert.pfx
SET /p pass=<%cd%\signtool\cert.txt
SET url=https://leomoon.com
SET app=%cd%\dist\%AppName%\%AppName%.exe
"%sign%" sign /fd SHA256 /d "%AppName%" /du "%url%" /f "%pfx%" /p %pass% /t "http://timestamp.comodoca.com/authenticode" "%app%"
::build setup
"C:\Program Files (x86)\Inno Setup 5\ISCC.exe" "%cd%\dist\setupgen.iss"
::sign setup
FOR %%i IN ("%cd%\dist\build\*.exe") DO SET setup=%%i
"%sign%" sign /fd SHA256 /d "%AppName% Setup" /du "%url%" /f "%pfx%" /p %pass% /t "http://timestamp.comodoca.com/authenticode" "%setup%"
explorer "%cd%\dist\build"
pause