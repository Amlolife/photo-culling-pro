import PyInstaller.__main__
import os

# Create a spec file content
spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
    ],
    hiddenimports=[
        'pyiqa',
        'pyiqa.archs',
        'pyiqa.archs.brisque',
        'pyiqa.archs.niqe',
        'pyiqa.archs.piqe',
        'pyiqa.utils',
        'pyiqa.data',
        'pyiqa.losses',
        'pyiqa.metrics',
        'torch',
        'torchvision',
        'cv2',
        'numpy',
        'PIL',
        'flask',
        'imagehash',
        'skimage',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    collect_all=['pyiqa'],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PhotoCullPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''

# Write the spec file
with open('PhotoCullPro.spec', 'w') as f:
    f.write(spec_content)

# Run PyInstaller with the spec
PyInstaller.__main__.run([
    '--clean',
    'PhotoCullPro.spec'
])
