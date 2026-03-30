# DOSBox-X Shortcut Generator

This script automates the creation of configurations and shortcuts for running `.hdi`-based games (or software) using DOSBox-X.

It is designed to simplify launching games directly from the Desktop by automatically generating:

- `.conf` configuration files
- `.ico` icons
- `.lnk` Windows shortcuts

---

## Features

- 🔍 Automatically detects `.hdi` files in folders
- 🖼️ Converts cover images into `.ico` icons
- ⚙️ Generates DOSBox-X compatible `.conf` files
- 🔗 Creates Desktop shortcuts
- 📁 Supports batch processing of multiple folders

---

## How It Works

For each provided folder:

1. **Search for `.hdi` file**
   - The first `.hdi` file found is selected

2. **Icon generation**
   - Searches for an image (`.jpg`, `.png`, `.webp`, etc.)
   - Resizes while preserving aspect ratio
   - Generates a multi-resolution `.ico` (up to 256x256)

3. **`.conf` file creation**
   - Uses a template defined in `config.toml`
   - Automatically mounts the `.hdi` image
   - Executes boot sequence

4. **Shortcut creation**
   - Generates a `.lnk` file on the Desktop
   - Launches DOSBox-X with the generated `.conf`
   - Applies custom icon if available

---

## Expected Folder Structure

Each folder should contain at least:

```
GameName/
├── game.hdi
├── cover.jpg   (optional)
```

---

## Configuration

The script uses a `config.toml` file for global settings.

### Example:

```toml
[SETTINGS]
dosbox_path = "C:\\DOSBox-X\\dosbox-x.exe"
conf_content = """
[dosbox]
machine=pc98

[sdl]
autolock=true
"""
```

### Parameters

- **dosbox_path**  
  Path to the DOSBox-X executable

- **conf_content**  
  Base content for the `.conf` file  
  (automatically extended with an `[autoexec]` section)

---

## Output

For each processed folder:

- `game.conf` → DOSBox-X configuration
- `icon.ico` → generated icon (if an image is found)
- `FolderName.lnk` → Desktop shortcut

---

## Usage

- Drag and drop one or more folders onto the script
- Or run it with folder paths as arguments

The script will automatically process each folder.

---

## PC-98 Visual Novel Collection (Torrent)

This repository also provides access to a large torrent archive (~76.79 GiB) containing a collection of PC-98 visual novels.

### Notes

- The archive is intended as a companion dataset for use with this tool
- Content organization is compatible with the expected folder structure
- Availability and download depend on torrent health (seeders/peers)
- Ensure you comply with local laws and regulations before downloading or using the content

---

## Notes

- If no image is found, the shortcut will be created without a custom icon
- Only the first `.hdi` file found is used
- Paths in `.conf` files are converted to POSIX format (`/`) for compatibility

---

## Requirements

- Windows operating system
- DOSBox-X installed

---

## Errors and Messages

- Missing `config.toml` → critical error with popup
- Missing `.hdi` → folder is skipped
- Image errors are reported but do not stop execution

---

## Purpose

This script is intended to streamline the management and launching of game collections (especially PC-98), reducing repetitive manual configuration work.

---
