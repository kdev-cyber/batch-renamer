# Batch Renamer

A safe Python file-renaming utility that previews rename changes before applying them.

This tool is designed for cleaning up messy folders by renaming supported files into a clean numbered sequence, such as:

```text
vacation_photo.jpg -> trip - 001.jpg
screenshot.png -> trip - 002.png
notes.pdf -> trip - 003.pdf
```

## Project Goal

The goal of this project is to create a practical automation tool that can rename groups of files safely and predictably.

Instead of immediately changing files, the script builds a rename plan, shows the user what will happen, and requires confirmation before live renaming.

## Features

* Rename files using a custom prefix
* Automatically number files in sequence
* Custom number padding, such as `001`, `002`, `003`
* Dry run mode for previewing changes without renaming anything
* Live rename confirmation using the exact word `RENAME`
* Duplicate-safe naming to prevent overwriting existing files
* Skips unsupported file types
* Skips folders automatically
* Friendly number input validation
* Creates a local rename log after each run

## Safety Features

This tool is built with safety in mind.

Before renaming files, it:

* Checks that the target folder exists
* Checks that the target path is actually a folder
* Validates number inputs
* Builds a rename plan before applying changes
* Shows the full rename plan to the user
* Requires explicit confirmation before live renaming
* Avoids overwriting existing files by adding `_DUPLICATE_1`, `_DUPLICATE_2`, etc.

## Supported File Types

```text
.jpg
.jpeg
.png
.gif
.webp
.mp4
.mkv
.mov
.avi
.txt
.pdf
.docx
```

## How to Run

From the project folder, run:

```powershell
python batch_renamer.py
```

The script will ask for:

```text
Target folder
Name prefix
Start number
Number padding
Dry run mode
```

## Example Dry Run

```text
=== Batch Renamer v3 ===

Enter target folder [C:\Users\K\Desktop\Rename_Test]:
Enter name prefix (leave blank for none) []: test
Start number [1]:
Number padding (e.g., 3 -> 001) [3]:
Dry run mode? Preview only, no changes. (y/n) [y]:

=== Rename Plan ===

[PLAN] photo.jpg -> test - 001.jpg
[PLAN] image.png -> test - 002.png

[MODE] Dry run enabled. No files will be renamed.

=== Results ===

[DRY RUN] photo.jpg -> test - 001.jpg
[DRY RUN] image.png -> test - 002.png

=== Summary ===
Files previewed: 2
Files skipped: 0
Done.
```

## Example Live Rename

To perform a live rename, choose `n` for dry run mode.

The script will show the rename plan first, then ask for confirmation:

```text
Type RENAME to confirm live rename []:
```

The rename only happens if the user types:

```text
RENAME
```

Any other response cancels the live rename.

## Log File

The script creates a local file called:

```text
rename_log.txt
```

This log records each run, including:

* Time of run
* Mode used
* Target folder
* Prefix
* Start number
* Padding
* Rename or preview results
* Summary counts

The log file is ignored by Git so local test logs do not get committed to the repository.

## Tech Used

* Python
* VS Code
* Git
* GitHub

## Project Status

Portfolio-ready command-line utility.

Completed:

* Dry run preview mode
* Live rename confirmation
* Rename plan before applying changes
* Duplicate-safe naming
* Number input validation
* Local rename logging
* Git ignore cleanup for generated logs

Planned improvements:

* Add screenshots of terminal output
* Add before-and-after example folder images
* Consider a simple GUI version later
