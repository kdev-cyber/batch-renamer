import os
from datetime import datetime
from helpers import get_input

# ===== INPUT HELPERS =====


def get_int_input(prompt, default):
    user_value = get_input(prompt, default)

    try:
        number = int(user_value)
    except ValueError:
        print(f"[ERROR] {prompt} must be a whole number.")
        exit()

    if number < 1:
        print(f"[ERROR] {prompt} must be 1 or higher.")
        exit()

    return number


print("\n=== Batch Renamer v2 ===\n")

# ===== INPUT =====

target_folder = get_input("Enter target folder", r"C:\Users\K\Desktop\Rename_Test")

prefix = get_input("Enter name prefix (leave blank for none)", "")

start_number = get_int_input("Start number", "1")

padding = get_int_input("Number padding (e.g., 3 -> 001)", "3")

dry_run = get_input("Dry run mode? Preview only, no changes. (y/n)", "y").lower() == "y"

# ===== SETTINGS =====

allowed_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".txt",
    ".pdf",
    ".docx",
)

script_folder = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_folder, "rename_log.txt")

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

    confirm = get_input("Type RENAME to confirm live rename", "")

    if confirm != "RENAME":
        print("[CANCELLED] Live rename was not confirmed.")
        exit()

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
log_entries = []

for file in files:
    old_path = os.path.join(target_folder, file)

    if os.path.isdir(old_path):
        message = f"[SKIP] Folder skipped: {file}"
        print(message)
        log_entries.append(message)
        skipped_count += 1
        continue

    base, ext = os.path.splitext(file)
    ext = ext.lower()

    if ext not in allowed_extensions:
        message = f"[SKIP] Unsupported file type: {file}"
        print(message)
        log_entries.append(message)
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
        message = f"[DRY RUN] {file} -> {safe_name}"
        print(message)
        log_entries.append(message)
    else:
        os.rename(old_path, new_path)
        message = f"[RENAME] {file} -> {safe_name}"
        print(message)
        log_entries.append(message)

    counter += 1
    renamed_count += 1

print("\n=== Summary ===")

if dry_run:
    summary_action = "previewed"
    print(f"Files previewed: {renamed_count}")
else:
    summary_action = "renamed"
    print(f"Files renamed: {renamed_count}")

print(f"Files skipped: {skipped_count}")
print("Done.\n")

with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write("\n=== Batch Renamer Run ===\n")
    log_file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write(f"Mode: {'DRY RUN' if dry_run else 'LIVE RENAME'}\n")
    log_file.write(f"Target folder: {target_folder}\n")
    log_file.write(f"Prefix: {prefix if prefix else '(none)'}\n")
    log_file.write(f"Start number: {start_number}\n")
    log_file.write(f"Padding: {padding}\n\n")

    for entry in log_entries:
        log_file.write(entry + "\n")

    log_file.write(f"\nFiles {summary_action}: {renamed_count}\n")
    log_file.write(f"Files skipped: {skipped_count}\n")
    log_file.write("Done.\n")
