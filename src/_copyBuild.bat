:: cleanup
rmdir ..\builds\ /s/q

::osx build copy
SET osBuild=osx
robocopy .\ ..\builds\%osBuild%\ *.py /v
robocopy lib\ ..\builds\%osBuild%\lib\ *.py /v /s
robocopy gui\ ..\builds\%osBuild%\gui\ *.py /v
robocopy gui\fonts\ ..\builds\%osBuild%\gui\fonts\ *.ttf /v
robocopy _fonts\ ..\builds\%osBuild%\dist\Fonts\ *.ttf /v
::os specific
robocopy .\ ..\builds\%osBuild%\ *.dylib /v
robocopy gui\icons\ ..\builds\%osBuild%\ main.icns /v
robocopy _bat\ ..\builds\%osBuild%\ _build.run /v
robocopy _setup\ ..\builds\%osBuild%\dist\ setupgen.pkgproj /v

::win build copy
SET osBuild=win
robocopy .\ ..\builds\%osBuild%\ *.py /v
robocopy lib\ ..\builds\%osBuild%\lib\ *.py /v /s
robocopy gui\ ..\builds\%osBuild%\gui\ *.py /v
robocopy gui\fonts\ ..\builds\%osBuild%\gui\fonts\ *.ttf /v
robocopy _fonts\ ..\builds\%osBuild%\dist\Fonts\ *.ttf /v
::os specific
robocopy .\ ..\builds\%osBuild%\ *.dll /v
robocopy .\ ..\builds\%osBuild%\ version.txt /v
robocopy gui\icons\ ..\builds\%osBuild%\ main.ico /v
robocopy _bat\ ..\builds\%osBuild%\ _build.bat /v
robocopy _setup\ ..\builds\%osBuild%\dist\ /XF setupgen.pkgproj /v
::sign
robocopy ..\..\..\#code-sign\signtool\ ..\builds\%osBuild%\signtool\ *.* /v

::lin build copy
SET osBuild=lin
robocopy .\ ..\builds\%osBuild%\ *.py /v
robocopy lib\ ..\builds\%osBuild%\lib\ *.py /v /s
robocopy gui\ ..\builds\%osBuild%\gui\ *.py /v
robocopy gui\fonts\ ..\builds\%osBuild%\gui\fonts\ *.ttf /v
robocopy _fonts\ ..\builds\%osBuild%\dist\Fonts\ *.ttf /v
::os specific
robocopy gui\icons\ ..\builds\%osBuild%\ main.ico /v
robocopy _bat\ ..\builds\%osBuild%\ _build.sh /v

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
cd ..\builds\win\
call _build.bat
:no
echo Goodbye
exit