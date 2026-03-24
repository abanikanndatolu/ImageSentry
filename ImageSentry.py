import os
import shutil
import hashlib
from PIL import Image
import imagehash

EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tiff')


# ---------------------------
# HASH FUNCTIONS
# ---------------------------

def get_file_hash(path):
    """Exact duplicate hash (fast, byte-level)"""
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_image_hash(path):
    """Perceptual hash for near duplicates"""
    try:
        img = Image.open(path)
        return imagehash.phash(img)
    except:
        return None


# ---------------------------
# QUALITY CHECK
# ---------------------------

def get_image_quality(path):
    """
    Score image quality based on:
    - Resolution
    - File size
    """
    try:
        img = Image.open(path)
        width, height = img.size
        file_size = os.path.getsize(path)

        # Simple scoring formula
        return (width * height) + file_size
    except:
        return 0


# ---------------------------
# MAIN DUPLICATE FINDER
# ---------------------------

def find_duplicates(folder, mode="exact", threshold=5):
    files = []

    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.lower().endswith(EXTENSIONS):
                files.append(os.path.join(root, f))

    groups = []
    visited = set()

    if mode == "exact":
        hash_map = {}

        for path in files:
            h = get_file_hash(path)
            hash_map.setdefault(h, []).append(path)

        for group in hash_map.values():
            if len(group) > 1:
                groups.append(group)

    elif mode == "near":
        hashes = []

        for path in files:
            h = get_image_hash(path)
            if h is not None:
                hashes.append((path, h))

        for i in range(len(hashes)):
            if i in visited:
                continue

            base_path, base_hash = hashes[i]
            group = [base_path]
            visited.add(i)

            for j in range(i + 1, len(hashes)):
                if j in visited:
                    continue

                path, h = hashes[j]

                if base_hash - h <= threshold:
                    group.append(path)
                    visited.add(j)

            if len(group) > 1:
                groups.append(group)

    return groups


# ---------------------------
# CLEANUP FUNCTION
# ---------------------------

def move_duplicates(groups, base_folder):
    dup_folder = os.path.join(base_folder, "duplicates")
    os.makedirs(dup_folder, exist_ok=True)

    for group in groups:
        # Sort by quality (highest first)
        sorted_group = sorted(group, key=get_image_quality, reverse=True)

        keep = sorted_group[0]
        duplicates = sorted_group[1:]

        print(f"\nKeeping: {os.path.basename(keep)}")

        for dup in duplicates:
            filename = os.path.basename(dup)
            new_path = os.path.join(dup_folder, filename)

            # Avoid overwrite
            counter = 1
            while os.path.exists(new_path):
                name, ext = os.path.splitext(filename)
                new_path = os.path.join(dup_folder, f"{name}_{counter}{ext}")
                counter += 1

            shutil.move(dup, new_path)
            print(f"Moved duplicate: {filename}")


# ---------------------------
# FORMAT OUTPUT
# ---------------------------

def print_groups(groups):
    print("\nDuplicate Groups:\n")
    for group in groups:
        base = os.path.basename(group[0])
        others = [os.path.basename(x) for x in group[1:]]
        print(f"{base}{{{', '.join(others)}}}")


# ---------------------------
# RUN
# ---------------------------

if __name__ == "__main__":
    print("ImageSentry - Duplicate Image Finder")
    print("=" * 50)
    folder = input("Enter folder path: ").strip()
    mode = input("Mode (exact/near): ").strip().lower()

    auto_clean = input("Move duplicates? (y/n): ").strip().lower() == "y"

    threshold = 5
    if mode == "near":
        threshold = int(input("Similarity threshold (default 5): ") or 5)

    groups = find_duplicates(folder, mode, threshold)

    print_groups(groups)

    if auto_clean:
        move_duplicates(groups, folder)
        print("\n✅ Duplicates moved to 'duplicates' folder.")
