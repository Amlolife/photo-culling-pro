import os
from pathlib import Path

import PyInstaller.__main__
from PyInstaller.utils.hooks import collect_submodules, collect_data_files


def build():
    project_root = Path(__file__).resolve().parent

    pyinstaller_args = [
        '--clean',
        '--name', 'PhotoCullPro',
        '--windowed',
        '--onefile',
        '--collect-all', 'pyiqa',
    ]

    data_paths = [
        (project_root / 'templates', 'templates'),
        (project_root / 'static', 'static'),
    ]

    pyiqa_data = collect_data_files('pyiqa', includes=['archs/*'])
    data_paths.extend(pyiqa_data)

    for src_path, dest_rel in data_paths:
        pyinstaller_args.extend([
            '--add-data', f'{src_path}{os.pathsep}{dest_rel}'
        ])

    hiddenimports = {
        'pyiqa',
        'pyiqa.archs',
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
    }
    hiddenimports.update(collect_submodules('pyiqa.archs'))

    for module in sorted(hiddenimports):
        pyinstaller_args.extend(['--hidden-import', module])

    pyinstaller_args.append(str(project_root / 'app.py'))

    PyInstaller.__main__.run([str(arg) for arg in pyinstaller_args])


if __name__ == '__main__':
    build()
