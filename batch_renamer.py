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


print("\n=== Batch Renamer v3 ===\n")

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

# ===== HELPERS =====


def get_safe_name(folder, filename, original_path, reserved_names):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1

    while True:
        candidate_path = os.path.join(folder, candidate)

        same_as_original = os.path.abspath(candidate_path) == os.path.abspath(
            original_path
        )
        already_exists = os.path.exists(candidate_path) and not same_as_original
        already_reserved = candidate.lower() in reserved_names

        if not already_exists and not already_reserved:
            return candidate

        candidate = f"{base}_DUPLICATE_{counter}{ext}"
        counter += 1


def write_log(mode_label, entries, summary_lines):
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write("\n=== Batch Renamer Run ===\n")
        log_file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Mode: {mode_label}\n")
        log_file.write(f"Target folder: {target_folder}\n")
        log_file.write(f"Prefix: {prefix if prefix else '(none)'}\n")
        log_file.write(f"Start number: {start_number}\n")
        log_file.write(f"Padding: {padding}\n\n")

        for entry in entries:
            log_file.write(entry + "\n")

        log_file.write("\n")
        for line in summary_lines:
            log_file.write(line + "\n")

        log_file.write("Done.\n")


# ===== BUILD RENAME PLAN =====

files = sorted(os.listdir(target_folder))

counter = start_number
skipped_count = 0
rename_plan = []
plan_entries = []
reserved_names = set()

for file in files:
    old_path = os.path.join(target_folder, file)

    if os.path.isdir(old_path):
        message = f"[SKIP] Folder skipped: {file}"
        plan_entries.append(message)
        skipped_count += 1
        continue

    base, ext = os.path.splitext(file)
    ext = ext.lower()

    if ext not in allowed_extensions:
        message = f"[SKIP] Unsupported file type: {file}"
        plan_entries.append(message)
        skipped_count += 1
        continue

    number = str(counter).zfill(padding)

    if prefix:
        new_name = f"{prefix} - {number}{ext}"
    else:
        new_name = f"{number}{ext}"

    safe_name = get_safe_name(target_folder, new_name, old_path, reserved_names)
    new_path = os.path.join(target_folder, safe_name)

    rename_plan.append(
        {
            "old_name": file,
            "new_name": safe_name,
            "old_path": old_path,
            "new_path": new_path,
        }
    )

    reserved_names.add(safe_name.lower())
    counter += 1


# ===== SHOW RENAME PLAN =====

print("\n=== Rename Plan ===\n")

for entry in plan_entries:
    print(entry)

for item in rename_plan:
    print(f"[PLAN] {item['old_name']} -> {item['new_name']}")

if not rename_plan:
    print("\nNo files to rename.")

    summary_lines = [
        "Files planned: 0",
        f"Files skipped: {skipped_count}",
    ]

    write_log("DRY RUN" if dry_run else "LIVE RENAME", plan_entries, summary_lines)

    print("\n=== Summary ===")
    print("Files planned: 0")
    print(f"Files skipped: {skipped_count}")
    print("Done.\n")
    exit()


# ===== CONFIRM LIVE RUN =====

if dry_run:
    print("\n[MODE] Dry run enabled. No files will be renamed.\n")
else:
    print("\n[MODE] Live run enabled. Files will be renamed.\n")

    confirm = get_input("Type RENAME to confirm live rename", "")

    if confirm != "RENAME":
        print("[CANCELLED] Live rename was not confirmed.")
        exit()


# ===== APPLY PLAN =====

result_entries = []

print("\n=== Results ===\n")

for item in rename_plan:
    if dry_run:
        message = f"[DRY RUN] {item['old_name']} -> {item['new_name']}"
    else:
        os.rename(item["old_path"], item["new_path"])
        message = f"[RENAME] {item['old_name']} -> {item['new_name']}"

    print(message)
    result_entries.append(message)


# ===== SUMMARY =====

print("\n=== Summary ===")

if dry_run:
    action_word = "previewed"
    print(f"Files previewed: {len(rename_plan)}")
else:
    action_word = "renamed"
    print(f"Files renamed: {len(rename_plan)}")

print(f"Files skipped: {skipped_count}")
print("Done.\n")

summary_lines = [
    f"Files {action_word}: {len(rename_plan)}",
    f"Files skipped: {skipped_count}",
]

write_log(
    "DRY RUN" if dry_run else "LIVE RENAME",
    plan_entries + result_entries,
    summary_lines,
)
