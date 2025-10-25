# Build Instructions for PhotoCullPro

## Problem Summary

The application was experiencing a `FileNotFoundError` when built with PyInstaller:
```
FileNotFoundError: [Errno 2] No such file or directory: 
'C:\\Users\\syari\\AppData\\Local\\Temp\\_MEI96482\\clip\\bpe_simple_vocab_16e6.txt.gz'
```

This occurred because:
1. **PyIQA** (image quality assessment library) dynamically imports various model architectures
2. Some architectures (CLIPIQA, LIQE) depend on the **CLIP** (Contrastive Language-Image Pre-training) model
3. CLIP requires data files (`bpe_simple_vocab_16e6.txt.gz`) that weren't being bundled by PyInstaller
4. The dynamic import happened at module load time, causing immediate failure

## Solution Implemented

### 1. **Lazy Loading of PyIQA Models**
- Changed from eager loading to lazy loading of IQA models
- Models are only initialized when actually needed
- Prevents CLIP import at application startup

### 2. **CLIP Module Exclusion**
- Updated `build_exe.py` to explicitly exclude CLIP-dependent modules:
  - `pyiqa.archs.clipiqa_arch`
  - `pyiqa.archs.clipiqa_plus_arch`
  - `pyiqa.archs.liqe_arch`
  - `pyiqa.archs.liqe_mix_arch`

### 3. **Import Patching**
- Created `pyiqa_patch.py` to intercept and block CLIP imports in frozen builds
- Applied automatically when running as a PyInstaller bundle

### 4. **Graceful Degradation**
- Application continues to work even if PyIQA models fail to load
- Uses fallback quality metrics based on OpenCV and traditional methods
- All core functionality (focus detection, exposure analysis, face detection) works without PyIQA

## Building the Application

### Prerequisites
```bash
pip install -r requirements.txt
```

### Build Command
```bash
python build_exe.py
```

This will:
1. Clean previous builds
2. Collect necessary data files (templates, static, OpenCV cascades)
3. Exclude CLIP and other problematic modules
4. Bundle only the required PyIQA architectures (BRISQUE, NIQE, PIQE)
5. Create a single executable: `dist/PhotoCullPro.exe`

### What Gets Bundled

**Included:**
- Flask templates and static files
- OpenCV Haar cascade files for face detection
- PyIQA models: BRISQUE, NIQE, PIQE (traditional metrics)
- All application dependencies

**Excluded:**
- CLIP model and dependencies
- CLIP-dependent PyIQA architectures
- Matplotlib (not needed)
- pytest, IPython (development tools)

## Testing the Build

1. **Run the executable:**
   ```bash
   dist\PhotoCullPro.exe
   ```

2. **Check the console output:**
   - Should see "PyIQA patch applied" if running from frozen build
   - Should not see CLIP-related errors
   - Flask server should start normally

3. **Test functionality:**
   - Upload images through the web interface
   - Verify image analysis works (focus, exposure, faces)
   - Check that quality scores are calculated

## Troubleshooting

### If PyIQA models still fail:
- The app will automatically fall back to OpenCV-based metrics
- Check console for warning messages
- Quality scores will still be calculated using focus and exposure analysis

### If other import errors occur:
1. Check `build_exe.py` hidden imports section
2. Add missing modules to the `hiddenimports` list
3. Rebuild the application

### If data files are missing:
1. Check the `--add-data` sections in `build_exe.py`
2. Verify paths exist before building
3. Use `--collect-all` for packages with many data files

## Architecture Notes

### Why Not Just Include CLIP?
- CLIP is a large model (~350MB)
- Has complex dependencies (ftfy, regex, tqdm)
- Requires specific data files that are hard to bundle
- Not essential for core photo culling functionality
- The traditional metrics (BRISQUE, NIQE, PIQE) work well without it

### Quality Metrics Used

**Without PyIQA:**
- Laplacian variance (focus/sharpness)
- Tenengrad gradient (edge sharpness)
- Histogram analysis (exposure)
- Face detection (OpenCV)

**With PyIQA (if available):**
- BRISQUE (Blind/Referenceless Image Spatial Quality Evaluator)
- NIQE (Natural Image Quality Evaluator)
- PIQE (Perception-based Image Quality Evaluator)

All metrics are traditional, non-deep-learning approaches that work reliably in frozen builds.

## Future Improvements

1. **Optional CLIP Support:**
   - Could add a separate "advanced" build with CLIP included
   - Would require custom PyInstaller hooks for CLIP data files

2. **Model Selection:**
   - Add UI option to enable/disable specific quality metrics
   - Allow users to choose between fast (OpenCV) and accurate (PyIQA) modes

3. **Progressive Enhancement:**
   - Download models on first run instead of bundling
   - Cache models in user directory for future use
