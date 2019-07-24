# -*- mode: python -*-

block_cipher = None


a = Analysis(['design\\code\\Face_Detection_Recognition-master\\04', 'faceRecognition\\faceRecognition\\ico\\man_student.ico', 'Start.py'],
             pathex=['E:\\graduation design\\code\\Face_Detection_Recognition-master\\04 faceRecognition\\faceRecognition'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='04',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='E:\\graduation')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='04')
