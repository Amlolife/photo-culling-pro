"""
Test script to verify imports work correctly before building.
"""

import sys
print(f"Python version: {sys.version}")
print(f"Frozen: {getattr(sys, 'frozen', False)}\n")

# Test basic imports
print("Testing basic imports...")
try:
    import cv2
    print(f"✓ OpenCV: {cv2.__version__}")
except ImportError as e:
    print(f"✗ OpenCV: {e}")

try:
    import numpy as np
    print(f"✓ NumPy: {np.__version__}")
except ImportError as e:
    print(f"✗ NumPy: {e}")

try:
    import PIL
    print(f"✓ Pillow: {PIL.__version__}")
except ImportError as e:
    print(f"✗ Pillow: {e}")

try:
    import flask
    print(f"✓ Flask: {flask.__version__}")
except ImportError as e:
    print(f"✗ Flask: {e}")

try:
    import imagehash
    print(f"✓ ImageHash: {imagehash.__version__}")
except ImportError as e:
    print(f"✗ ImageHash: {e}")

# Test PyIQA
print("\nTesting PyIQA...")
try:
    import pyiqa
    print(f"✓ PyIQA imported successfully")
    
    # Try to create a simple metric (not CLIP-dependent)
    try:
        model = pyiqa.create_metric('brisque', device='cpu')
        print(f"✓ BRISQUE model created successfully")
    except Exception as e:
        print(f"✗ BRISQUE model creation failed: {e}")
    
except ImportError as e:
    print(f"✗ PyIQA: {e}")

# Test CLIP (should be available in dev, excluded in build)
print("\nTesting CLIP (optional)...")
try:
    import clip
    print(f"✓ CLIP imported (will be excluded in build)")
except ImportError as e:
    print(f"✗ CLIP not available: {e}")

# Test app imports
print("\nTesting app.py imports...")
try:
    # This will trigger the pyiqa_patch if frozen
    import app
    print(f"✓ app.py imported successfully")
    print(f"  - PYIQA_AVAILABLE: {app.PYIQA_AVAILABLE}")
    print(f"  - TORCH_AVAILABLE: {app.TORCH_AVAILABLE}")
except Exception as e:
    print(f"✗ app.py import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("Import test complete!")
print("="*50)
