# Wordlist Finder – Recursive Text Search Tool

**Wordlist Finder** is a lightweight desktop utility for developers and analysts.
It recursively scans files in a folder for a specific keyword and shows matching lines with file path and line number.

Built with Python and Tkinter, this standalone tool requires no installation or setup – and can be exported as a `.exe`.

---

## Features

* Folder selection via UI dialog
* Customizable file extensions (e.g. `.py`, `.env`, `.json`)
* Fast recursive keyword search
* Line preview with match highlight
* Integrated result viewer
* Optional `.exe` export for Windows
* Modern UI Version with `customtkinter` and PDF support

---

## Use Cases

* Search for `API_KEY`, `token`, or `password` in projects
* Detect `TODO` / `FIXME` tags in source code
* Audit `.env`, `.yaml`, or `.json` configs
* Explore large folder structures without a terminal

---

## Getting Started

the modernwordsearch.py needs (modern UI + PDF support):
```bash
pip install customtkinter pymupdf
```


```bash
python wordsearch.py
```

No dependencies, no setup – just run.

---

## Build as Windows `.exe`

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed wordlist-finder.py
```

➡️ Output will be in `/dist/wordlist-finder.exe`