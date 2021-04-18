:: cleanup
rmdir ..\build\ /s/q

::osx build copy
SET osBuild=osx
robocopy .\ ..\build\%osBuild%\ *.py /v
robocopy lib\ ..\build\%osBuild%\lib\ *.py /v /s
robocopy gui\ ..\build\%osBuild%\gui\ *.py /v
robocopy gui\fonts\ ..\build\%osBuild%\gui\fonts\ *.ttf /v
robocopy _fonts\ ..\build\%osBuild%\dist\Fonts\ *.ttf /v
::os specific
robocopy .\ ..\build\%osBuild%\ *.dylib /v
robocopy gui\icons\ ..\build\%osBuild%\ main.icns /v
robocopy _bat\ ..\build\%osBuild%\ _build.run /v
robocopy _setup\ ..\build\%osBuild%\dist\ setupgen.pkgproj /v

::win build copy
SET osBuild=win
robocopy .\ ..\build\%osBuild%\ *.py /v
robocopy lib\ ..\build\%osBuild%\lib\ *.py /v /s
robocopy gui\ ..\build\%osBuild%\gui\ *.py /v
robocopy gui\fonts\ ..\build\%osBuild%\gui\fonts\ *.ttf /v
robocopy _fonts\ ..\build\%osBuild%\dist\Fonts\ *.ttf /v
::os specific
robocopy .\ ..\build\%osBuild%\ *.dll /v
robocopy .\ ..\build\%osBuild%\ version.txt /v
robocopy gui\icons\ ..\build\%osBuild%\ main.ico /v
robocopy _bat\ ..\build\%osBuild%\ _build.bat /v
robocopy _setup\ ..\build\%osBuild%\dist\ /XF setupgen.pkgproj /v
::sign
robocopy ..\..\..\#code-sign\signtool\ ..\build\%osBuild%\signtool\ *.* /v

::lin build copy
SET osBuild=lin
robocopy .\ ..\build\%osBuild%\ *.py /v
robocopy lib\ ..\build\%osBuild%\lib\ *.py /v /s
robocopy gui\ ..\build\%osBuild%\gui\ *.py /v
robocopy gui\fonts\ ..\build\%osBuild%\gui\fonts\ *.ttf /v
robocopy _fonts\ ..\build\%osBuild%\dist\Fonts\ *.ttf /v
::os specific
robocopy gui\icons\ ..\build\%osBuild%\ main.ico /v
robocopy _bat\ ..\build\%osBuild%\ _build.sh /v

::version change before build
@echo off
cd ..
call _sreplace.bat

::ask to build for windows
@echo off
:ask
echo Do you want to build for Windows? (Y/N)
SET INPUT=
SET /P INPUT=Type input: %=%
If /I "%INPUT%"=="y" goto yes 
If /I "%INPUT%"=="n" goto no
echo Incorrect input & goto ask
:yes
cd ..\build\win\
call _build.bat
:no
echo Goodbye
exit