# TIFF Converter - Grayscale & Compress

A cross-platform GUI application for converting TIFF images to grayscale with ZIP compression while preserving all metadata tags.

## Features

- **RGB-Only Filter**: Automatically skips grayscale images; only processes RGB/RGBA files
- **Grayscale Conversion**: Converts RGB/RGBA images to grayscale using ITU-R 601-2 standard luminosity weighting
- **Compression**: Applies ZIP (Deflate) compression to reduce file size
- **Metadata Preservation**: Preserves all TIFF tags including custom SEM device metadata
- **Batch Processing**: Convert single files or entire folder trees recursively
- **Cross-Platform**: Works on Windows and Linux
- **File Count Preview**: Shows how many TIFFs will be processed before starting
- **Cancellation Support**: Pause/cancel long conversions anytime
- **Multiple Output Modes**:
  - **Add Suffix**: Adds a suffix to filename (e.g., `image_gray_compressed.tif`)
  - **Output Folder**: Save all converted files to a specified folder
  - **Replace Original**: Overwrite the original files
- **Settings Persistence**: Remembers your last settings

## Installation

### Option 1: Standalone Executable (Linux Mint 22.3)

No Python or dependencies required! Download a pre-built executable:

1. **Download from GitHub Actions:**
   - Go to the [Releases](../../releases) page
   - Download `tiff-comp` or `tiff-comp-linux-x64.tar.gz`

2. **Run directly:**
   ```bash
   chmod +x tiff-comp
   ./tiff-comp
   ```

**See [BUILD_LINUX.md](BUILD_LINUX.md) for detailed build instructions or to build your own executable.**

---

### Option 2: Python Installation (Manual Setup)

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Create and activate virtual environment** (recommended):

**Windows (PowerShell):**
```powershell
python -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### GUI Application (Recommended)

**Windows:**
```powershell
python gui.py
```

**Linux:**
```bash
python3 gui.py
```

#### GUI Workflow

1. **Select Input**: Click "Browse File" for a single TIFF or "Browse Folder" for batch processing
2. **Choose Output Mode**:
   - **Add Suffix**: Enter suffix (default: `_gray_compressed`)
   - **Output Folder**: Select destination folder for converted files; the source subfolder structure is replicated there
   - **Replace Original**: Overwrite source files in place, keeping the same path
3. **Select Compression Method**:
   - **No Compression**: Larger files, faster processing, lossless
   - **ZIP/Deflate** (default): Recommended - good compression ratio, widely compatible
   - **LZW**: Alternative compression, good for archival
4. **Preview & Convert**: Click "Convert" to see file count and confirm before processing starts
5. **Monitor**: Watch progress bar and log for detailed status
6. **Cancel Anytime**: Use the "Cancel" button to stop ongoing conversion; already processed files are kept

### Command Line (Advanced)

For single file conversion (uses default ZIP compression):
```bash
python convert_tif.py input.tif output.tif
```

Example:
```bash
python convert_tif.py sample/A1_005.tif sample/A1_005_gray_compressed.tif
```

**Note:** To use different compression methods, use the GUI or modify the Python code to call `convert_and_compress(input, output, compression='method')` where method is `'zlib'` (default), `'lzw'`, or `'none'`.

#### Batch Convert (PowerShell)

```powershell
Get-ChildItem -Path sample -Filter *.tif | ForEach-Object {
  $in = $_.FullName
  $out = Join-Path $_.DirectoryName ($_.BaseName + '_gray_compressed.tif')
  python convert_tif.py $in $out
}
```

#### Batch Convert (Linux Bash)

```bash
for file in sample/*.tif; do
  output="${file%.*}_gray_compressed.tif"
  python3 convert_tif.py "$file" "$output"
done
```

## Files

- **`gui.py`** - Tkinter GUI application (cross-platform)
- **`convert_tif.py`** - Core conversion engine
- **`requirements.txt`** - Python dependencies
- **`gui_settings.json`** - Auto-saved settings (created on first GUI run)
- **`utils/compare_tags.py`** - Debug utility to inspect and compare TIFF tags
- **`sample/`** - Example TIFF files for testing

## Conversion Details

### RGB Filter
- **Only RGB/RGBA images are processed** (3 or 4 channels)
- Grayscale images (2D arrays) are automatically skipped with a message
- Other formats are also skipped
- In batch mode, skipped files are reported in the log
- Allows safe batch processing of mixed image types

### Grayscale Algorithm
Uses standard ITU-R 601-2 luminosity weights:
- Red: 0.2989
- Green: 0.5870
- Blue: 0.1140

### Compression Details

**Supported Methods:**

| Method | Size | Speed | Compatibility | Best For |
|--------|------|-------|---------------|-----------| 
| **Uncompressed** | Largest | Fastest | Universal | Maximum compatibility, archival |
| **ZIP/Deflate** | Medium | Fast | Excellent | Default choice, good balance |
| **LZW** | Medium | Fast | Good | Scientific images, archival |

- **Uncompressed**: No compression applied; files are larger but decode faster
- **ZIP (Deflate)**: Standard lossless compression, best balance of size and compatibility
- **LZW**: Lempel-Ziv-Welch compression; good for images with repetitive patterns

All methods preserve image quality (lossless compression - no data loss).

### Metadata Handling
- Preserves resolution information (XResolution, YResolution, ResolutionUnit)
- Preserves custom tags (e.g., FEI SEM metadata)
- Complex metadata values (dicts, nested structures) are JSON-encoded for storage
- Automatically filters out non-portable structural tags (ImageWidth, ImageLength, etc.)

## Troubleshooting

### Module Not Found Error
If you get `ModuleNotFoundError: No module named 'numpy'` or `'tifffile'`:
```bash
pip install -r requirements.txt
```

### No TIFF Files Found
Ensure your folder contains `.tif` or `.tiff` files. The tool searches recursively through all subfolders.

### Files Skipped During Batch Processing
The tool automatically skips:
- **Grayscale images** (2D arrays with shape like `(height, width)`)
- **Non-RGB/RGBA formats** (single channel, 5+ channels, etc.)
- Non-TIFF files

This is intentional to ensure only RGB images are converted. Check the log for detailed skip reasons.

### Permission Denied (Replace Mode)
If "Replace Original" fails, check that:
- The original file is not open in another application
- You have write permissions to the folder

### GUI Not Appearing (Linux)
If tkinter is not available, install it:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

## Metadata Preservation Example

**Original TIFF tags:**
- ImageWidth, ImageLength, BitsPerSample, Compression, PhotometricInterpretation
- XResolution, YResolution, ResolutionUnit
- **Custom**: FEI_HELIOS (SEM device metadata)

**After Conversion:**
- All standard tags preserved
- FEI_HELIOS and other custom tags preserved (JSON-encoded if complex)
- Resolution information maintained
- New compression tag added (ZIP)

## Performance

## Development & Debugging

### Compare TIFF Tags
To inspect and compare metadata tags between original and converted files:

```bash
python utils/compare_tags.py original.tif converted.tif
```

This utility outputs side-by-side tag listings for debugging metadata handling.

- Single 2000×2000 8-bit RGB image: ~1-2 seconds
- Folder with 10 images: ~10-20 seconds
- File size reduction: 30-60% typical (varies by image content)

## Limitations

- Input must be valid TIFF format
- Output is always grayscale 8-bit or 16-bit (depends on input)
- Very large files (>2GB) may require significant memory

## License

See project documentation for license information.

## Support

For issues or feature requests, refer to project documentation or contact the development team.
