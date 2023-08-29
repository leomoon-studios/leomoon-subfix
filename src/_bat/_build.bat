@REM cleanup old build if any
SET AppName=LeoMoon SubFix
rmdir "%cd%\dist\build\" /s/q
rmdir "%cd%\dist\%AppName%\" /s/q
rmdir "%cd%\__pycache__\" /s/q
@REM build python
C:\Python\python -m PyInstaller --add-binary *.dll;. --clean --windowed --onedir --noupx --name "%AppName%" --version-file=version.txt --icon=main.ico main.py
@REM cleanup
rmdir "%cd%\dist\%AppName%\PyQt5\Qt\translations\" /s/q
@REM prepare
if not exist "%cd%\dist\%AppName%\" mkdir "%cd%\dist\%AppName%\"
if exist "%cd%\dist\%AppName%.exe" move "%cd%\dist\%AppName%.exe" "%cd%\dist\%AppName%\"
@REM sign app
timeout /t 1 /nobreak
SET sign=%cd%\signtool\signtool.exe
SET pfx=%cd%\signtool\cert.pfx
SET /p pass=<%cd%\signtool\cert.txt
SET url=https://leomoon.com
SET app=%cd%\dist\%AppName%\%AppName%.exe
"%sign%" sign /fd SHA256 /d "%AppName%" /du "%url%" /f "%pfx%" /p %pass% /t "http://timestamp.comodoca.com/authenticode" "%app%"
@REM build setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "%cd%\dist\setupgen.iss"
@REM sign setup
timeout /t 1 /nobreak
FOR %%i IN ("%cd%\dist\build\*.exe") DO SET setup=%%i
"%sign%" sign /fd SHA256 /d "%AppName% Setup" /du "%url%" /f "%pfx%" /p %pass% /t "http://timestamp.comodoca.com/authenticode" "%setup%"
explorer "%cd%\dist\build"
pause
