# 📁 ImageSentry

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ImageSentry** is a powerful Python utility designed to keep your photo library clean and organized. It detects both **exact duplicates** (byte-for-byte matches) and **near duplicates** (visually similar images) using perceptual hashing.

When cleaning up, it intelligently preserves the **highest quality version** (based on resolution and file size) and can automatically move duplicates to a separate folder.

---

## 🚀 Features

- **Exact Detection**: Finds identical files using MD5 hashing.
- **Visual Similarity**: Uses `pHash` to detect images that have been resized, compressed, or renamed.
- **Auto-Cleanup**: Automatically organizes duplicates into a dedicated folder.
- **Quality-First Retention**: Keeps the version with the best resolution and file size.
- **Wide Format Support**: Works with `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.webp`, and `.tiff`.

---

## 🛠️ Requirements

- Python 3.8 or higher
- [Pillow](https://pypi.org/project/Pillow/) (Image processing)
- [ImageHash](https://pypi.org/project/ImageHash/) (Perceptual hashing)

### Installation

Install the required dependencies via pip:

```bash
pip install pillow imagehash
```

---

## ⚡ Usage Guide

### 1. Setup
Clone the repository and navigate to the project folder:
```bash
git clone https://github.com/abanikanndatolu/ImageSentry.git
cd ImageSentry
```

### 2. Execution
Run the main script:
```bash
python imagesentry.py
```

### 3. Interaction
Follow the interactive prompts:

- **Folder Path**: Enter the path to the directory you want to scan.
  - *Example:* `/home/user/Pictures`
- **Mode Selection**:
  - `exact`: Detects byte-for-byte identical files.
  - `near`: Detects visually similar images (useful for finding resized copies).
- **Auto-Clean**:
  - `y`: Moves duplicates to a `duplicates/` subfolder.
  - `n`: Only displays duplicates without moving them.
- **Threshold (Near Mode Only)**:
  - Default: `5`
  - *Stricter:* Lower values (e.g., `2`)
  - *Lenient:* Higher values (e.g., `10`)

---

## 🔧 How It Works

### Exact Mode
Computes a unique MD5 hash for every file. If two files have the same hash, they are guaranteed to be identical at the byte level.

### Near Mode
Utilizes **Perceptual Hashing (pHash)**. This generates a "fingerprint" of the image based on its visual features rather than its raw data. This allows the tool to identify images even if they have different resolutions or file formats.

### Quality Scoring
For every group of duplicates detected, ImageSentry calculates a score based on:
1.  **Resolution**: Higher width/height is preferred.
2.  **File Size**: Larger file size (at the same resolution) often implies less compression.

The image with the highest score is kept in place, while others are flagged as duplicates.

---

## 🗂 Project Structure

```text
ImageSentry/
├── imagesentry.py    # Core logic and script entry
├── README.md         # Documentation
└── duplicates/       # Created automatically if auto-clean is used
```

---

## 💡 Example

```text
Enter folder path: /home/user/Pictures
Mode (exact/near): near
Move duplicates? (y/n): y
Similarity threshold (default 5): 5

Duplicate Groups:
image1.png {copy1.png, duplicate.jpg, resized.webp}
photo.png {photo_copy.png, edited.png}

✅ Duplicates successfully moved to the 'duplicates' folder.
```

---

## ✅ Best Practices & Notes

- **Initial Run**: If you're unsure, run in `near` mode with `Move duplicates? (n)` first to see what would be grouped.
- **Performance**: For massive libraries (10,000+ items), the `near` mode might take a few minutes as it needs to process every image.
- **Refinement**: Adjust the threshold if you find the tool is grouping images that are too different.

---

## 🔗 Future Enhancements

- [ ] **Graphical User Interface (GUI)** for easier drag-and-drop usage.
- [ ] **Multi-threaded processing** to speed up large scans.
- [ ] **AI-driven Quality Assessment** for even smarter preservation.
- [ ] **Cloud/Network drive scanning** support.
