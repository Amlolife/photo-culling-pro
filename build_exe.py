import os
import sys
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
        '--noconfirm',
    ]

    # Add templates and static files
    data_paths = [
        (project_root / 'templates', 'templates'),
        (project_root / 'static', 'static'),
    ]

    # Collect OpenCV cascade files
    try:
        import cv2
        cv2_data = Path(cv2.__file__).parent / 'data'
        if cv2_data.exists():
            pyinstaller_args.extend([
                '--add-data', f'{cv2_data}{os.pathsep}cv2/data'
            ])
    except Exception as e:
        print(f"Warning: Could not collect cv2 data: {e}")

    # Try to collect CLIP data files if available
    try:
        clip_data = collect_data_files('clip', includes=['*.txt.gz', '*.pt'])
        if clip_data:
            for src, dest in clip_data:
                pyinstaller_args.extend([
                    '--add-data', f'{src}{os.pathsep}{dest}'
                ])
            print(f"Collected {len(clip_data)} CLIP data files")
    except Exception as e:
        print(f"Warning: Could not collect CLIP data files: {e}")

    # Collect PyIQA data files (excluding CLIP-dependent architectures)
    try:
        pyiqa_data = collect_data_files('pyiqa')
        if pyiqa_data:
            for src, dest in pyiqa_data:
                pyinstaller_args.extend([
                    '--add-data', f'{src}{os.pathsep}{dest}'
                ])
            print(f"Collected {len(pyiqa_data)} PyIQA data files")
    except Exception as e:
        print(f"Warning: Could not collect PyIQA data: {e}")

    # Add user data paths
    for src_path, dest_rel in data_paths:
        if Path(src_path).exists():
            pyinstaller_args.extend([
                '--add-data', f'{src_path}{os.pathsep}{dest_rel}'
            ])
    
    # Add pyiqa_patch module
    patch_file = project_root / 'pyiqa_patch.py'
    if patch_file.exists():
        pyinstaller_args.extend([
            '--add-data', f'{patch_file}{os.pathsep}.'
        ])

    # Hidden imports - only include what we actually use
    hiddenimports = [
        'cv2',
        'numpy',
        'PIL',
        'PIL.Image',
        'flask',
        'imagehash',
        'skimage',
        'skimage.measure',
        'sqlite3',
        'werkzeug',
    ]

    # Conditionally add PyIQA imports
    try:
        import pyiqa
        hiddenimports.extend([
            'pyiqa',
            'pyiqa.archs',
            'pyiqa.utils',
            'pyiqa.data',
        ])
        # Collect only non-CLIP architectures
        pyiqa_archs = collect_submodules('pyiqa.archs')
        # Exclude CLIP-dependent modules
        excluded_archs = [
            'pyiqa.archs.clipiqa_arch',
            'pyiqa.archs.clipiqa_plus_arch',
            'pyiqa.archs.liqe_arch',
            'pyiqa.archs.liqe_mix_arch',
        ]
        pyiqa_archs = [m for m in pyiqa_archs if m not in excluded_archs]
        hiddenimports.extend(pyiqa_archs)
    except ImportError:
        print("Warning: PyIQA not available, skipping PyIQA imports")

    # Add torch if available
    try:
        import torch
        hiddenimports.extend(['torch', 'torch.nn'])
    except ImportError:
        print("Warning: PyTorch not available")

    # Add hidden imports
    for module in hiddenimports:
        pyinstaller_args.extend(['--hidden-import', module])

    # Exclude problematic modules
    exclude_modules = [
        'clip',  # Exclude CLIP to avoid data file issues
        'matplotlib',
        'pytest',
        'IPython',
    ]
    for module in exclude_modules:
        pyinstaller_args.extend(['--exclude-module', module])

    # Add runtime hook
    hook_file = project_root / 'hook-pyiqa.py'
    if hook_file.exists():
        pyinstaller_args.extend(['--runtime-hook', str(hook_file)])

    # Add the main script
    pyinstaller_args.append(str(project_root / 'app.py'))

    print("\nBuilding with PyInstaller...")
    print(f"Arguments: {' '.join(str(arg) for arg in pyinstaller_args)}\n")

    PyInstaller.__main__.run([str(arg) for arg in pyinstaller_args])


if __name__ == '__main__':
    build()
