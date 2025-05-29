# -*- mode: python ; coding: utf-8 -*-

# 本文件用于打包 Windows 程序
# https://pyinstaller.org/en/stable/spec-files.html
# https://pyinstaller.org/en/stable/advanced-topics.html#the-toc-and-tree-classes
# pip install pyinstaller
# pyinstaller --clean --noconfirm build_exe.spec
import time
import re

pattern_binary = "Qt5|Qt6Pdf.dll|Qt6Network.dll|opengl32sw.dll"
regex_binary = re.compile(pattern_binary)
pattern_data = "Qt5|-info"
regex_data = re.compile(pattern_data)

block_cipher = None

start = time.time()
print("start",start)
a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('resources', 'resources')],
             hiddenimports=['PyQt5','bcrypt'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['./lanzou/login_assister.py','PyQtWebEngine','PyQt5','PIL','bcrypt'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# 移除无关dll 和 data
a.binaries = [x for x in a.binaries if regex_binary.search(x[0]) is None]
a.datas = [x for x in a.datas if regex_data.search(x[0]) is None]
print("binaries",time.time() -start, a.binaries)
print("datas",time.time()-start, a.datas)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
print("pyz",time.time()-start, pyz)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='lanzou-gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          version='./version_info.txt',
          icon='./app_icon.ico')
print("exe",time.time()-start, exe)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[
                    'vcruntime140.dll',
                    'vcruntime140_1.dll',
                    'msvcp140_1.dll',
                    'msvcp140.dll',
                    'python3.dll',
                    '_uuid.pyd',
                    'opengl32sw.dll',
                ],
               name='lanzou-gui')

print("coll", time.time()-start, coll)
