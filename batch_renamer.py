import os
from helpers import get_input

print("\n=== Batch Renamer v2 ===\n")

# ===== INPUT =====

target_folder = get_input(
    "Enter target folder",
    r"C:\Users\K\Desktop\Rename_Test"
)

prefix = get_input(
    "Enter name prefix (leave blank for none)",
    ""
)

start_number = int(get_input(
    "Start number",
    "1"
))

padding = int(get_input(
    "Number padding (e.g., 3 -> 001)",
    "3"
))

dry_run = get_input(
    "Dry run mode? Preview only, no changes. (y/n)",
    "y"
).lower() == "y"

# ===== SETTINGS =====

allowed_extensions = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".mp4", ".mkv", ".mov", ".avi",
    ".txt", ".pdf", ".docx"
)

# ===== VALIDATION =====

if not os.path.exists(target_folder):
    print("[ERROR] Folder does not exist.")
    exit()

if not os.path.isdir(target_folder):
    print("[ERROR] Target path is not a folder.")
    exit()

if dry_run:
    print("\n[MODE] Dry run enabled. No files will be renamed.\n")
else:
    print("\n[MODE] Live run enabled. Files will be renamed.\n")

# ===== HELPERS =====

def get_safe_name(folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1

    while os.path.exists(os.path.join(folder, candidate)):
        candidate = f"{base}_DUPLICATE_{counter}{ext}"
        counter += 1

    return candidate


# ===== MAIN LOGIC =====

files = sorted(os.listdir(target_folder))

counter = start_number
renamed_count = 0
skipped_count = 0

for file in files:
    old_path = os.path.join(target_folder, file)

    if os.path.isdir(old_path):
        print(f"[SKIP] Folder skipped: {file}")
        skipped_count += 1
        continue

    base, ext = os.path.splitext(file)
    ext = ext.lower()

    if ext not in allowed_extensions:
        print(f"[SKIP] Unsupported file type: {file}")
        skipped_count += 1
        continue

    number = str(counter).zfill(padding)

    if prefix:
        new_name = f"{prefix} - {number}{ext}"
    else:
        new_name = f"{number}{ext}"

    safe_name = get_safe_name(target_folder, new_name)
    new_path = os.path.join(target_folder, safe_name)

    if dry_run:
        print(f"[DRY RUN] {file} -> {safe_name}")
    else:
        os.rename(old_path, new_path)
        print(f"[RENAME] {file} -> {safe_name}")

    counter += 1
    renamed_count += 1

print("\n=== Summary ===")
print(f"Files renamed: {renamed_count}")
print(f"Files skipped: {skipped_count}")
print("Done.\n")