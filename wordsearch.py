import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class WordlistFinderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔍 Wordlist Finder")
        self.geometry("720x740")
        self.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.export_path = tk.StringVar()
        self.keyword = tk.StringVar()
        self.extensions = [".py", ".txt", ".env", ".md", ".json"]

        self.progress = tk.DoubleVar(value=0)

        self.build_ui()

    def build_ui(self):
        padding = {"padx": 20, "pady": 10}

        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", **padding)
        ttk.Label(header, text="🔍 Wordlist Finder", font=("Segoe UI", 20, "bold")).pack(anchor="center")

        # Main Frame
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=30, pady=10)

        # Folder selection
        self.build_path_selector(main, "Search Folder", self.folder_path, self.browse_folder)

        # Export file path
        self.build_path_selector(main, "Export File", self.export_path, self.choose_export_file)

        # Keyword input
        ttk.Label(main, text="Keyword to search for:", font=("Segoe UI", 11)).pack(anchor="w", pady=(10, 0))
        ttk.Entry(main, textvariable=self.keyword, width=60).pack(fill="x")

        # File extensions
        ttk.Label(main, text="File Extensions (comma-separated):", font=("Segoe UI", 11)).pack(anchor="w", pady=(10, 0))
        self.ext_entry = tk.Text(main, height=2, width=60)
        self.ext_entry.insert("1.0", ", ".join(self.extensions))
        self.ext_entry.pack(fill="x")

        # Start button
        ttk.Button(main, text="Start Search", command=self.start_search).pack(pady=15)

        # Progress bar
        ttk.Progressbar(main, variable=self.progress, maximum=1).pack(fill="x", pady=5)
        self.progress_label = ttk.Label(main, text="", foreground="gray")
        self.progress_label.pack()

        # Results
        ttk.Label(main, text="Search Results:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.result_box = tk.Text(main, wrap="word", height=20)
        self.result_box.pack(fill="both", expand=True, pady=(5, 5))

        # Export Button
        ttk.Button(main, text="Export Results", command=self.export_results).pack(pady=(0, 10))

        # Footer
        ttk.Label(self, text="Created by: https://github.com/1Jul1an", foreground="gray").pack(side="bottom", pady=5)

    def build_path_selector(self, parent, label, var, command):
        ttk.Label(parent, text=label + ":", font=("Segoe UI", 11)).pack(anchor="w", pady=(10, 0))
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        ttk.Entry(frame, textvariable=var, width=60).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ttk.Button(frame, text="Browse", command=command).pack(side="right")

    def browse_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.folder_path.set(selected)

    def choose_export_file(self):
        selected = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if selected:
            self.export_path.set(selected)

    def start_search(self):
        folder = self.folder_path.get()
        export_file = self.export_path.get()
        keyword = self.keyword.get().strip()
        ext_raw = self.ext_entry.get("1.0", "end").strip()
        self.result_box.delete("1.0", "end")
        self.progress.set(0)

        if not folder or not keyword:
            messagebox.showerror("Error", "Please provide both folder and keyword.")
            return

        extensions = [ext.strip() for ext in ext_raw.split(",") if ext.strip().startswith(".")]
        matches = []

        file_list = []
        for root_dir, _, files in os.walk(folder):
            for name in files:
                if any(name.lower().endswith(ext) for ext in extensions):
                    file_list.append(os.path.join(root_dir, name))

        total = len(file_list)
        if total == 0:
            self.result_box.insert("end", "No files found with the selected extensions.")
            return

        for i, path in enumerate(file_list):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if keyword.lower() in line.lower():
                            matches.append(f"{path}:{line_num}: {line.strip()}")
            except (UnicodeDecodeError, PermissionError):
                continue

            self.progress.set((i + 1) / total)
            self.progress_label.config(text=f"{i + 1}/{total} files scanned")

        if matches:
            self.result_box.insert("end", "\n".join(matches))
        else:
            self.result_box.insert("end", "No matches found.")

        # Auto-export
        if export_file:
            self.save_to_file(export_file, matches)

    def export_results(self):
        content = self.result_box.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Nothing to Export", "There are no search results.")
            return

        export_file = self.export_path.get()
        if not export_file:
            self.choose_export_file()
            export_file = self.export_path.get()

        if not export_file:
            return

        self.save_to_file(export_file, content.splitlines())

    def save_to_file(self, file_path, lines):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Export Successful", f"Results saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred:\n{e}")

if __name__ == "__main__":
    app = WordlistFinderApp()
    app.mainloop()
