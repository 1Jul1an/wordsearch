import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF

class WordlistFinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔍 Wordlist Finder")
        self.geometry("760x800")
        self.resizable(False, False)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.folder_path = ctk.StringVar()
        self.export_path = ctk.StringVar()
        self.keyword = ctk.StringVar()
        self.extensions = [".py", ".txt", ".env", ".md", ".json", ".pdf"]

        self.progress = ctk.DoubleVar(value=0)

        self.build_ui()

    def build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        ctk.CTkLabel(header, text="🔍 Wordlist Finder", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")

        self.theme_switch = ctk.CTkSwitch(header, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="right")
        self.theme_switch.select()

        # Main content
        main = ctk.CTkFrame(self, corner_radius=12)
        main.pack(fill="both", expand=True, padx=30, pady=15)

        # Folder Selection
        self.build_path_selector(main, "Search Folder", self.folder_path, self.browse_folder)

        # Export File Selection
        self.build_path_selector(main, "Export to File", self.export_path, self.choose_export_file)

        # Keyword input
        ctk.CTkLabel(main, text="Keyword", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 3))
        ctk.CTkEntry(main, textvariable=self.keyword, placeholder_text="Enter keyword to search for...", height=38).pack(fill="x")

        # File extensions
        ctk.CTkLabel(main, text="File Extensions (comma-separated)", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(15, 3))
        self.ext_text = ctk.CTkTextbox(main, height=40)
        self.ext_text.insert("1.0", ", ".join(self.extensions))
        self.ext_text.pack(fill="x")

        # Start button
        ctk.CTkButton(main, text="🔎 Start Search", command=self.start_search, height=45).pack(pady=20)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main, variable=self.progress, height=14)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 8))

        # Results Label
        ctk.CTkLabel(main, text="Search Results", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 0))

        # Results box
        self.result_box = ctk.CTkTextbox(main, wrap="word", height=250, font=ctk.CTkFont(size=13))
        self.result_box.pack(fill="both", expand=True, pady=(5, 5))

        # Export Button
        ctk.CTkButton(main, text="💾 Export Results to File", command=self.export_results).pack(pady=(10, 5))

        # Footer
        ctk.CTkLabel(self, text="Created by: https://github.com/1Jul1an", font=ctk.CTkFont(size=12), text_color="gray").pack(side="bottom", pady=8)

    def build_path_selector(self, parent, label_text, path_var, command):
        ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 3))
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.pack(fill="x", pady=3)
        ctk.CTkEntry(path_frame, textvariable=path_var, placeholder_text="Choose path...", height=38).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(path_frame, text="Browse", width=100, command=command).pack(side="right")

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")

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
        ext_raw = self.ext_text.get("1.0", "end").strip()
        self.result_box.delete("1.0", "end")
        self.progress.set(0)

        if not folder or not keyword:
            messagebox.showerror("Error", "Please provide both a folder and keyword.")
            return

        extensions = [ext.strip() for ext in ext_raw.split(",") if ext.strip().startswith(".")]
        matches = []

        file_list = []
        for root_dir, _, files in os.walk(folder):
            for name in files:
                if any(name.lower().endswith(ext.lower()) for ext in extensions):
                    file_list.append(os.path.join(root_dir, name))

        total = len(file_list)
        if total == 0:
            self.result_box.insert("end", "No files found with selected extensions.")
            return

        for i, path in enumerate(file_list):
            try:
                if path.lower().endswith(".pdf"):
                    doc = fitz.open(path)
                    for page_num, page in enumerate(doc, 1):
                        text = page.get_text()
                        for line_num, line in enumerate(text.splitlines(), 1):
                            if keyword.lower() in line.lower():
                                matches.append(f"{path} [Page {page_num}]: {line.strip()}")
                else:
                    with open(path, "r", encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            if keyword.lower() in line.lower():
                                matches.append(f"{path}:{line_num}: {line.strip()}")
            except (UnicodeDecodeError, PermissionError, RuntimeError):
                continue

            self.progress.set((i + 1) / total)

        if matches:
            self.result_box.insert("end", "\n".join(matches))
        else:
            self.result_box.insert("end", "No matches found.")

        # Auto-export if export path is already selected
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
            return  # user cancelled

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
