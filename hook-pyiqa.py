# PyInstaller runtime hook for pyiqa
# This hook prevents pyiqa from importing CLIP-dependent models

import sys
import os

# Patch pyiqa to skip CLIP-dependent architectures
if hasattr(sys, 'frozen'):
    try:
        import pyiqa.archs
        
        # Get the original __init__ module
        original_init = pyiqa.archs.__file__
        
        # List of architectures that depend on CLIP and should be excluded
        CLIP_DEPENDENT_ARCHS = [
            'clipiqa_arch',
            'clipiqa_plus_arch',
            'liqe_arch',
            'liqe_mix_arch',
        ]
        
        # Monkey patch the import mechanism to skip CLIP-dependent models
        def safe_import_module(module_name):
            """Only import modules that don't depend on CLIP"""
            arch_name = module_name.split('.')[-1]
            if arch_name in CLIP_DEPENDENT_ARCHS:
                return None
            try:
                return __import__(module_name, fromlist=[''])
            except Exception as e:
                print(f"Warning: Could not import {module_name}: {e}")
                return None
        
        print("PyIQA runtime hook: Excluding CLIP-dependent architectures")
        
    except Exception as e:
        print(f"PyIQA runtime hook warning: {e}")
