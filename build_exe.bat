@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Building EXE...
pyinstaller ascii2png.spec --noconfirm --clean

echo Done! Output is in dist/ASCII2PNG.exe
pause
