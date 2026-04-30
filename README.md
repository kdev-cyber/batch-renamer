\# Batch Renamer v2



A simple Python tool to rename files in bulk with consistent numbering, prefixes, and safe preview mode.



\---



\## 🚀 Features



\- Rename multiple files instantly

\- Optional name prefix (e.g., `Vacation - 001.png`)

\- Automatic numbering with padding (001, 002, 003…)

\- Dry run mode (preview changes before applying)

\- Skips folders automatically

\- Skips unsupported file types

\- Prevents duplicate filename conflicts

\- Clean summary output after execution



\---



\## 🧠 How It Works



The script scans a target folder and renames files in order using:



\- A customizable prefix

\- A starting number

\- Zero-padded numbering format



\### Example



\*\*Before:\*\*

```

Screenshot 1.png

video.mkv

notes.txt

```



\*\*After:\*\*

```

Vacation - 001.png

Vacation - 002.mkv

Vacation - 003.txt

```



\---



\## ⚙️ Usage



1\. Run the script:

```

python batch\_renamer.py

```



2\. Enter the required inputs:

\- Target folder path

\- Optional prefix

\- Start number

\- Number padding

\- Dry run mode (y/n)



\---



\## 🔍 Dry Run Mode (Recommended)



Use dry run mode (`y`) to preview changes before applying them.



Example:

```

\[DRY RUN] file.png -> Vacation - 001.png

```



No files will be changed in this mode.



\---



\## ⚡ Live Mode



Set dry run to `n` to apply changes:



```

\[RENAME] file.png -> Vacation - 001.png

```



\---



\## 📁 Supported File Types



\- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`

\- Videos: `.mp4`, `.mkv`, `.mov`, `.avi`

\- Documents: `.txt`, `.pdf`, `.docx`



\---



\## 🛡 Safety Features



\- Skips folders automatically

\- Skips unsupported file types

\- Prevents overwriting existing files by creating unique names



\---



\## 🧾 Example Output



```

=== Summary ===

Files renamed: 3

Files skipped: 1

Done.

```



\---



\## 📌 Notes



\- Files are renamed in sorted order

\- Prefix is optional (leave blank for numbering only)

\- Existing renamed files may be processed again if rerun



\---



\## 🔮 Future Improvements



\- Remember last-used settings (persistent config)

\- Skip already formatted filenames

\- Custom file type filters

\- GUI version



\---



\## 👨‍💻 Author



Built as part of a growing Python automation toolkit focused on real-world file management and workflow optimization.

