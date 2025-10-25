"""
Patch for pyiqa to prevent CLIP-dependent model imports in frozen builds.
This module should be imported before pyiqa to prevent import errors.
"""

import sys
import importlib.util

# List of CLIP-dependent architecture modules to block
BLOCKED_MODULES = [
    'pyiqa.archs.clipiqa_arch',
    'pyiqa.archs.clipiqa_plus_arch',
    'pyiqa.archs.liqe_arch',
    'pyiqa.archs.liqe_mix_arch',
]

# Store the original import function
_original_import = __builtins__.__import__

def _patched_import(name, globals=None, locals=None, fromlist=(), level=0):
    """
    Patched import function that blocks CLIP-dependent modules.
    """
    # Check if this is a blocked module
    if name in BLOCKED_MODULES:
        # Return a dummy module to prevent import errors
        dummy_module = type(sys)('dummy_' + name.split('.')[-1])
        sys.modules[name] = dummy_module
        return dummy_module
    
    # Also check if we're importing 'clip' from within pyiqa
    if name == 'clip' and globals and globals.get('__name__', '').startswith('pyiqa'):
        # Block CLIP import from within pyiqa
        raise ImportError(f"CLIP import blocked from {globals.get('__name__', 'unknown')}")
    
    # Otherwise, use the original import
    return _original_import(name, globals, locals, fromlist, level)

def apply_patch():
    """Apply the import patch to block CLIP-dependent modules."""
    if getattr(sys, 'frozen', False):
        # Only apply patch in frozen (PyInstaller) builds
        __builtins__.__import__ = _patched_import
        print("PyIQA patch applied: CLIP-dependent modules will be blocked")

def remove_patch():
    """Remove the import patch."""
    __builtins__.__import__ = _original_import
    print("PyIQA patch removed")
