import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onedir',
    '--windowed',
    '-n Camlive',
])