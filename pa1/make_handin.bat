c:\python27\scripts\pyinstaller -w -F -i src\icon.ico src\GUI.py

mkdir submit
mkdir submit\src
mkdir submit\test

copy src\* submit\src\*
copy test\* submit\test\*
copy dist\GUI.exe submit\DES-GUI.exe

pause