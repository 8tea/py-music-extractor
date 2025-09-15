#!/usr/bin/env python3
"""
Music Library Extractor - Complete Application

A complete GUI application for extracting music zip files from Downloads folder
and organizing them into the proper music library structure.

Double-click this file to run the application.
"""

import os
import sys
import zipfile
import shutil
import re
import threading
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import logging

# Suppress console window on Windows when running as GUI
if sys.platform.startswith('win'):
    import ctypes
    try:
        # Hide console window
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# Configure ttk styles for modern look
def configure_styles():
    style = ttk.Style()
    
    # Configure modern theme
    style.theme_use('clam')
    
    # Configure custom styles with elegant white/black theme
    style.configure('Title.TLabel', 
                   font=('Segoe UI', 18, 'bold'),
                   foreground='#000000',
                   background='#ffffff')
    
    style.configure('Subtitle.TLabel',
                   font=('Segoe UI', 10),
                   foreground='#333333',
                   background='#ffffff')
    
    style.configure('Modern.TFrame',
                   background='#ffffff',
                   relief='flat')
    
    style.configure('TFrame',
                   background='#ffffff')
    
    style.configure('Card.TLabelFrame',
                   background='#ffffff',
                   relief='solid',
                   borderwidth=1,
                   bordercolor='#f0f0f0')
    
    style.configure('TLabelFrame',
                   background='#ffffff')
    
    style.configure('Card.TLabelFrame.Label',
                   font=('Segoe UI', 11, 'bold'),
                   foreground='#000000',
                   background='#ffffff')
    
    # Map the LabelFrame style
    style.map('Card.TLabelFrame',
              background=[('active', '#ffffff'),
                         ('focus', '#ffffff')],
              bordercolor=[('active', '#e8e8e8'),
                          ('focus', '#e8e8e8')])
    
    style.configure('Modern.TButton',
                   font=('Segoe UI', 9, 'bold'),
                   padding=(15, 8),
                   relief='flat',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#ffffff',
                   foreground='#000000')
    
    style.map('Modern.TButton',
              background=[('active', '#f0f0f0'),
                         ('pressed', '#e0e0e0')],
              foreground=[('active', '#000000'),
                         ('pressed', '#000000')])
    
    style.configure('Primary.TButton',
                   font=('Segoe UI', 9, 'bold'),
                   padding=(20, 8),
                   relief='flat',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#000000',
                   foreground='#ffffff')
    
    style.map('Primary.TButton',
              background=[('active', '#333333'),
                         ('pressed', '#666666')],
              foreground=[('active', '#ffffff'),
                         ('pressed', '#ffffff')])
    
    style.configure('Success.TButton',
                   font=('Segoe UI', 9, 'bold'),
                   padding=(20, 8),
                   relief='flat',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#28a745',
                   foreground='#ffffff')
    
    style.map('Success.TButton',
              background=[('active', '#34ce57'),
                         ('pressed', '#1e7e34')],
              foreground=[('active', '#ffffff'),
                         ('pressed', '#ffffff')])
    
    style.configure('Danger.TButton',
                   font=('Segoe UI', 9, 'bold'),
                   padding=(15, 8),
                   relief='flat',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#ffffff',
                   foreground='#000000')
    
    style.map('Danger.TButton',
              background=[('active', '#f0f0f0'),
                         ('pressed', '#e0e0e0')],
              foreground=[('active', '#000000'),
                         ('pressed', '#000000')])
    
    style.configure('Compact.TButton',
                   font=('Segoe UI', 8),
                   padding=(8, 6),
                   relief='flat',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#ffffff',
                   foreground='#000000')
    
    style.map('Compact.TButton',
              background=[('active', '#f0f0f0'),
                         ('pressed', '#e0e0e0')],
              foreground=[('active', '#000000'),
                         ('pressed', '#000000')])
    
    style.configure('Disabled.TButton',
                   font=('Segoe UI', 9, 'bold'),
                   padding=(20, 8),
                   relief='flat',
                   borderwidth=1,
                   bordercolor='#cccccc',
                   background='#f5f5f5',
                   foreground='#999999')
    
    style.map('Disabled.TButton',
              background=[('active', '#f5f5f5'),
                         ('pressed', '#f5f5f5'),
                         ('disabled', '#f5f5f5')],
              foreground=[('active', '#999999'),
                         ('pressed', '#999999'),
                         ('disabled', '#999999')])
    
    style.configure('Modern.TEntry',
                   font=('Segoe UI', 10),
                   padding=(10, 8),
                   relief='solid',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#ffffff',
                   foreground='#000000')
    
    style.configure('Modern.TCombobox',
                   font=('Segoe UI', 10),
                   padding=(10, 8),
                   relief='solid',
                   borderwidth=1,
                   bordercolor='#000000',
                   background='#ffffff',
                   foreground='#000000')
    
    style.configure('Modern.TProgressbar',
                   background='#000000',
                   troughcolor='#f0f0f0',
                   borderwidth=1,
                   bordercolor='#000000',
                   lightcolor='#000000',
                   darkcolor='#000000')
    
    return style

# Create a custom logging handler for the GUI
class GUILogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

class MusicExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Library Extractor")
        self.root.geometry("750x600")
        self.root.configure(bg='#ffffff')
        self.root.resizable(True, True)
        
        # Configure modern styles
        self.style = configure_styles()
        
        # Center the window on screen
        self.center_window()
        
        # Configuration - user can modify these
        self.downloads_folder = os.path.expanduser("~/Downloads")
        self.music_library_path = "~/Music"  # Changed to just /Music for cleaner structure
        
        # Settings file path
        self.settings_file = os.path.join(os.path.expanduser("~"), ".music_extractor_settings.json")
        
        # Setup logging first (before load_settings which might use logger)
        self.setup_logging()
        
        # Format patterns - user can select from dropdown (define before load_settings)
        self.format_patterns = {
            "Artist - Album.zip": r"^(.+?)\s*-\s*(.+?)\.zip$",
            "Artist_Album.zip": r"^(.+?)_(.+?)\.zip$",
            "Artist.Album.zip": r"^(.+?)\.(.+?)\.zip$",
            "Album by Artist.zip": r"^(.+?)\s+by\s+(.+?)\.zip$",
            "Artist - Album - Year.zip": r"^(.+?)\s*-\s*(.+?)\s*-\s*\d{4}\.zip$"
        }
        self.current_pattern = "Artist - Album.zip"
        self.zip_pattern = self.format_patterns[self.current_pattern]
        
        # Load saved settings (after patterns are defined)
        self.load_settings()
        
        # Create GUI
        self.create_widgets()
        
    def setup_logging(self):
        """Setup logging to display in GUI"""
        # Configure logging
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Add GUI handler (will be set after text widget is created)
        self.gui_handler = None
        
    def create_widgets(self):
        """Create the GUI widgets with modern design"""
        # Main container with modern styling
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # Compact header with title and format selection
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky=(tk.W, tk.E))
        header_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="🎵 Music Extractor", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        # Format selection (compact)
        ttk.Label(header_frame, text="Format:", font=('Segoe UI', 9)).grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.format_var = tk.StringVar(value=self.current_pattern)
        format_combo = ttk.Combobox(header_frame, textvariable=self.format_var, 
                                   values=list(self.format_patterns.keys()),
                                   state='readonly', style='Modern.TCombobox', width=20)
        format_combo.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # Add dropdown indicator
        ttk.Label(header_frame, text="▼", font=('Segoe UI', 8), foreground='#666666').grid(row=0, column=3, sticky=tk.W)
        
        # Compact settings area
        settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="8")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8))
        settings_frame.columnconfigure((0, 2), weight=1)
        
        # Downloads folder (compact)
        ttk.Label(settings_frame, text="Downloads:", font=('Segoe UI', 9)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.downloads_var = tk.StringVar(value=self.downloads_folder)
        downloads_entry = ttk.Entry(settings_frame, textvariable=self.downloads_var, 
                                   style='Modern.TEntry')
        downloads_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 3))
        ttk.Button(settings_frame, text="📁", style='Compact.TButton',
                  command=self.browse_downloads_folder).grid(row=0, column=2)
        
        # Extract folder (compact)
        ttk.Label(settings_frame, text="Extract to:", font=('Segoe UI', 9)).grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.music_lib_var = tk.StringVar(value=self.music_library_path)
        music_lib_entry = ttk.Entry(settings_frame, textvariable=self.music_lib_var,
                                   style='Modern.TEntry')
        music_lib_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 3), pady=(5, 0))
        ttk.Button(settings_frame, text="📁", style='Compact.TButton',
                  command=self.browse_music_library).grid(row=1, column=2, pady=(5, 0))
        
        # Auto delete checkbox
        self.auto_delete_var = tk.BooleanVar(value=True)  # Checked by default
        auto_delete_check = ttk.Checkbutton(settings_frame, text="Auto delete zip after extracting", 
                                          variable=self.auto_delete_var, 
                                          command=self.on_auto_delete_change)
        auto_delete_check.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Compact action area
        action_frame = ttk.Frame(self.main_frame)
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8))
        action_frame.columnconfigure(0, weight=1)
        
        # Statistics (compact)
        stats_frame = ttk.Frame(action_frame)
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.files_found_label = ttk.Label(stats_frame, text="Found: 0", 
                                          font=('Segoe UI', 8), foreground='#000000')
        self.files_found_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.files_processed_label = ttk.Label(stats_frame, text="Processed: 0", 
                                              font=('Segoe UI', 8), foreground='#000000')
        self.files_processed_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.files_failed_label = ttk.Label(stats_frame, text="Failed: 0", 
                                           font=('Segoe UI', 8), foreground='#000000')
        self.files_failed_label.pack(side=tk.LEFT)
        
        # Action buttons (compact)
        button_frame = ttk.Frame(action_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure((0, 1, 2), weight=1)  # Equal weight for all columns
        
        self.scan_button = ttk.Button(button_frame, text="🔍 Scan", 
                                     command=self.scan_music_zips, style='Primary.TButton')
        self.scan_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 2))
        
        self.extract_button = ttk.Button(button_frame, text="📦 Extract", 
                                        command=self.extract_all, state=tk.DISABLED, style='Disabled.TButton')
        self.extract_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 2))
        
        
        self.open_folder_button = ttk.Button(button_frame, text="📂 Open Extraction Folder", 
                                            command=self.open_extract_folder, style='Modern.TButton')
        self.open_folder_button.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # Progress bar (compact)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(action_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Status (compact)
        self.status_frame = ttk.Frame(action_frame)
        self.status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.status_frame.columnconfigure(1, weight=1)  # Allow message to expand
        
        self.status_icon = ttk.Label(self.status_frame, text="", font=('Segoe UI', 12))
        self.status_icon.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.status_message = ttk.Label(self.status_frame, text="Ready to scan", 
                                       font=('Segoe UI', 9), foreground='#000000')
        self.status_message.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Create expandable output section (initially hidden)
        self.create_expandable_section()
        
        # Setup GUI logging handler (after log_text is created)
        self.gui_handler = GUILogHandler(self.log_text)
        self.gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.gui_handler)
        
        # Store found music zips
        self.music_zips = []
        
        # Expandable section state (always expanded now)
        self.expanded = True
        
        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        
    def create_expandable_section(self):
        """Create the expandable output section"""
        # Create expandable frame
        self.expandable_frame = ttk.LabelFrame(self.main_frame, text="📋 Output", padding="8")
        self.expandable_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 0))
        self.expandable_frame.columnconfigure(0, weight=1)
        self.expandable_frame.rowconfigure(1, weight=1)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.expandable_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Found files tab
        files_frame = ttk.Frame(notebook)
        notebook.add(files_frame, text="📋 Found Files")
        
        # Create treeview for file preview
        columns = ('Artist', 'Album', 'Filename')
        self.file_tree = ttk.Treeview(files_frame, columns=columns, show='headings', height=3)
        
        # Configure columns
        self.file_tree.heading('Artist', text='Artist')
        self.file_tree.heading('Album', text='Album')
        self.file_tree.heading('Filename', text='Filename')
        
        self.file_tree.column('Artist', width=120, minwidth=100)
        self.file_tree.column('Album', width=150, minwidth=120)
        self.file_tree.column('Filename', width=200, minwidth=150)
        
        # Add scrollbar for treeview
        tree_scroll = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Grid the treeview and scrollbar
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Activity log tab
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="📝 Activity Log")
        
        # Modern text area styling
        self.log_text = scrolledtext.ScrolledText(log_frame, height=5,
                                                 font=('Consolas', 9), 
                                                 bg='#ffffff', fg='#000000', 
                                                 insertbackground='#000000',
                                                 selectbackground='#000000',
                                                 selectforeground='white',
                                                 relief='flat', borderwidth=1,
                                                 highlightthickness=1,
                                                 highlightcolor='#000000')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Keep the expandable section always visible
        
            
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common operations"""
        # Bind Ctrl+S for scan
        self.root.bind('<Control-s>', lambda e: self.scan_music_zips())
        # Bind Ctrl+E for extract
        self.root.bind('<Control-e>', lambda e: self.extract_all() if self.extract_button['state'] != 'disabled' else None)
        # Bind F5 for refresh/scan
        self.root.bind('<F5>', lambda e: self.scan_music_zips())
        
    def save_settings(self):
        """Save current settings to file"""
        settings = {
            'downloads_folder': self.downloads_folder,
            'music_library_path': self.music_library_path,
            'current_pattern': self.current_pattern,
            'auto_delete_zip': self.auto_delete_var.get()
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Could not save settings: {e}")
            else:
                print(f"Could not save settings: {e}")
            
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.downloads_folder = settings.get('downloads_folder', self.downloads_folder)
                    self.music_library_path = settings.get('music_library_path', self.music_library_path)
                    
                    # Load pattern setting and update zip_pattern
                    saved_pattern = settings.get('current_pattern', self.current_pattern)
                    if saved_pattern in self.format_patterns:
                        self.current_pattern = saved_pattern
                        self.zip_pattern = self.format_patterns[self.current_pattern]
                    
                    # Load auto_delete setting, default to True if not found
                    auto_delete_setting = settings.get('auto_delete_zip', True)
                    if hasattr(self, 'auto_delete_var'):
                        self.auto_delete_var.set(auto_delete_setting)
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Could not load settings: {e}")
            else:
                print(f"Could not load settings: {e}")
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def browse_downloads_folder(self):
        """Browse for downloads folder"""
        folder = filedialog.askdirectory(initialdir=self.downloads_folder)
        if folder:
            self.downloads_var.set(folder)
            self.downloads_folder = folder
            self.save_settings()
            
    def browse_music_library(self):
        """Browse for music library folder"""
        folder = filedialog.askdirectory(initialdir=self.music_library_path)
        if folder:
            self.music_lib_var.set(folder)
            self.music_library_path = folder
            self.save_settings()
            
    def on_auto_delete_change(self):
        """Handle auto delete checkbox change"""
        auto_delete = self.auto_delete_var.get()
        self.logger.info(f"Auto delete zip files: {'Enabled' if auto_delete else 'Disabled'}")
        self.save_settings()
            
    def open_extract_folder(self):
        """Open the extract folder in file manager"""
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                os.startfile(self.music_library_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.music_library_path])
            else:  # Linux
                subprocess.run(["xdg-open", self.music_library_path])
        except Exception as e:
            self.logger.error(f"Could not open folder: {e}")
            messagebox.showerror("Error", f"Could not open folder: {e}")
            
        
    def populate_file_tree(self):
        """Populate the file preview tree with found music zips"""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # Add found files to tree
        for zip_info in self.music_zips:
            self.file_tree.insert('', 'end', values=(
                zip_info['artist'],
                zip_info['album'],
                zip_info['filename']
            ))
        
    def update_status(self, icon, message, color='black'):
        """Update the status notification"""
        self.status_icon.config(text=icon)
        self.status_message.config(text=message, foreground=color)
        
    def show_success(self, message):
        """Show success notification with checkmark"""
        self.update_status("✅", message, '#000000')
        
    def show_error(self, message):
        """Show error notification with X mark"""
        self.update_status("❌", message, '#000000')
        
    def show_processing(self, message):
        """Show processing notification with spinner"""
        self.update_status("⏳", message, '#000000')
        
    def show_extraction_loading(self):
        """Show animated extraction loading indicator"""
        # Create loading dialog
        self.loading_dialog = tk.Toplevel(self.root)
        self.loading_dialog.title("Extracting...")
        self.loading_dialog.geometry("300x150")
        self.loading_dialog.configure(bg='#ffffff')
        self.loading_dialog.resizable(False, False)
        
        # Center the dialog
        self.loading_dialog.transient(self.root)
        self.loading_dialog.grab_set()
        
        # Center on parent window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        self.loading_dialog.geometry(f"300x150+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(self.loading_dialog, bg='#ffffff', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Loading icon
        self.loading_icon = tk.Label(main_frame, text="⏳", font=('Segoe UI', 24), 
                                    bg='#ffffff', fg='#000000')
        self.loading_icon.pack(pady=(0, 10))
        
        # Loading text
        loading_text = tk.Label(main_frame, text="Extracting music files...", 
                               font=('Segoe UI', 12, 'bold'), 
                               bg='#ffffff', fg='#000000')
        loading_text.pack(pady=(0, 5))
        
        # Progress text
        self.progress_text = tk.Label(main_frame, text="Please wait...", 
                                     font=('Segoe UI', 10), 
                                     bg='#ffffff', fg='#666666')
        self.progress_text.pack()
        
        # Start spinner animation
        self.spinner_frames = ["⏳", "⏲", "⏰", "⏱"]
        self.spinner_index = 0
        self.animate_spinner()
        
    def animate_spinner(self):
        """Animate the spinner icon"""
        if hasattr(self, 'loading_dialog') and self.loading_dialog.winfo_exists():
            self.loading_icon.config(text=self.spinner_frames[self.spinner_index])
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
            self.loading_dialog.after(500, self.animate_spinner)
            
    def hide_extraction_loading(self):
        """Hide the extraction loading dialog"""
        if hasattr(self, 'loading_dialog') and self.loading_dialog.winfo_exists():
            self.loading_dialog.destroy()
        
    def show_success_dialog(self, processed, failed, extracted_files=None):
        """Show a custom success dialog with green styling and countdown timer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Extraction Complete")
        dialog.geometry("500x450")
        dialog.configure(bg='#28a745')  # Green background to match theme
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center on parent window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 225
        dialog.geometry(f"500x450+{x}+{y}")
        
        # Main frame with green background
        main_frame = tk.Frame(dialog, bg='#28a745', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Success icon and title
        icon_label = tk.Label(main_frame, text="✅", font=('Segoe UI', 24), 
                             bg='#28a745', fg='#ffffff')
        icon_label.pack(pady=(0, 10))
        
        title_label = tk.Label(main_frame, text="Extraction Complete!", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#28a745', fg='#ffffff')
        title_label.pack(pady=(0, 15))
        
        # Success message
        success_text = f"Successfully processed {processed} file{'s' if processed != 1 else ''}"
        success_label = tk.Label(main_frame, text=success_text, 
                                font=('Segoe UI', 12), 
                                bg='#28a745', fg='#ffffff')
        success_label.pack(pady=(0, 10))
        
        # Only show failed count if there were failures
        if failed > 0:
            failed_text = f"Failed to process {failed} file{'s' if failed != 1 else ''}"
            failed_label = tk.Label(main_frame, text=failed_text, 
                                   font=('Segoe UI', 12), 
                                   bg='#28a745', fg='#ffcccb')  # Light red on green
            failed_label.pack(pady=(0, 10))
        
        # Extracted files list
        if extracted_files and len(extracted_files) > 0:
            # Header for extracted files
            files_header = tk.Label(main_frame, text="Extracted files:", 
                                   font=('Segoe UI', 11, 'bold'), 
                                   bg='#28a745', fg='#ffffff')
            files_header.pack(pady=(10, 5), anchor='w')
            
            # Create a frame for the scrollable list
            list_frame = tk.Frame(main_frame, bg='#28a745')
            list_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Create a canvas and scrollbar for the file list
            canvas = tk.Canvas(list_frame, bg='#28a745', highlightthickness=0, height=120)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#28a745')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add extracted files to the list
            for i, file_info in enumerate(extracted_files):
                # Create destination path
                dest_path = os.path.join(self.music_library_path, file_info['artist'], file_info['album'])
                
                # File info frame
                file_frame = tk.Frame(scrollable_frame, bg='#28a745')
                file_frame.pack(fill=tk.X, pady=2)
                
                # Artist - Album
                artist_album = f"{file_info['artist']} - {file_info['album']}"
                artist_label = tk.Label(file_frame, text=artist_album, 
                                      font=('Segoe UI', 9, 'bold'), 
                                      bg='#28a745', fg='#ffffff', anchor='w')
                artist_label.pack(fill=tk.X, padx=(0, 5))
                
                # Destination path
                path_label = tk.Label(file_frame, text=f"→ {dest_path}", 
                                    font=('Segoe UI', 8), 
                                    bg='#28a745', fg='#e8f5e8', anchor='w')  # Light green
                path_label.pack(fill=tk.X, padx=(10, 5))
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # Close button below the output section
        close_button = tk.Button(main_frame, text="Close", 
                                command=dialog.destroy,
                                font=('Segoe UI', 9, 'bold'),
                                bg='#28a745', fg='#000000',
                                relief='flat', borderwidth=1,
                                padx=20, pady=8)
        close_button.pack(pady=(15, 5), anchor='center')
        
        # Focus on close button
        close_button.focus_set()
        
        # Bind Enter key to close dialog
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        
    def on_format_change(self, event):
        """Handle format dropdown selection change"""
        selected_format = self.format_var.get()
        if selected_format in self.format_patterns:
            self.current_pattern = selected_format
            self.zip_pattern = self.format_patterns[selected_format]
            self.logger.info(f"Format changed to: {selected_format}")
            self.show_success(f"Format updated to: {selected_format}")
            self.save_settings()
            
            
    def open_extract_folder(self):
        """Open the extract folder in file manager"""
        import subprocess
        import platform
        
        folder_path = self.music_lib_var.get()
        if os.path.exists(folder_path):
            try:
                if platform.system() == "Windows":
                    os.startfile(folder_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", folder_path])
                else:  # Linux
                    subprocess.run(["xdg-open", folder_path])
                self.logger.info(f"Opened folder: {folder_path}")
            except Exception as e:
                self.logger.error(f"Could not open folder: {e}")
                messagebox.showerror("Error", f"Could not open folder: {e}")
        else:
            messagebox.showwarning("Folder Not Found", f"Folder does not exist: {folder_path}")
            
    def update_statistics(self, found=0, processed=0, failed=0):
        """Update the statistics display"""
        self.files_found_label.config(text=f"Found: {found}")
        self.files_processed_label.config(text=f"Processed: {processed}")
        self.files_failed_label.config(text=f"Failed: {failed}")
        
    def validate_paths(self):
        """Validate that the configured paths exist and are accessible"""
        errors = []
        
        # Check downloads folder
        if not os.path.exists(self.downloads_folder):
            errors.append(f"Downloads folder does not exist: {self.downloads_folder}")
        elif not os.access(self.downloads_folder, os.R_OK):
            errors.append(f"No read access to downloads folder: {self.downloads_folder}")
            
        # Check music library path
        if not os.path.exists(self.music_library_path):
            try:
                os.makedirs(self.music_library_path, exist_ok=True)
                self.logger.info(f"Created music library directory: {self.music_library_path}")
            except Exception as e:
                errors.append(f"Cannot create music library directory: {self.music_library_path} - {e}")
        elif not os.access(self.music_library_path, os.W_OK):
            errors.append(f"No write access to music library folder: {self.music_library_path}")
            
        return errors
        
    def scan_music_zips(self):
        """Scan for music zip files"""
        self.downloads_folder = self.downloads_var.get()
        self.music_library_path = self.music_lib_var.get()
        
        # Validate paths first
        path_errors = self.validate_paths()
        if path_errors:
            error_msg = "Path validation failed:\n" + "\n".join(path_errors)
            self.logger.error(error_msg)
            self.show_error("Path validation failed. Check the log for details.")
            messagebox.showerror("Path Error", error_msg)
            return
        
        self.show_processing("Scanning for music zip files...")
        self.logger.info("Scanning for music zip files...")
        self.music_zips = self.find_music_zips()
        
        if self.music_zips:
            self.logger.info(f"Found {len(self.music_zips)} music zip files")
            self.show_success(f"Found {len(self.music_zips)} files ready to extract")
            self.extract_button.config(state=tk.NORMAL, style='Success.TButton')
            self.update_statistics(found=len(self.music_zips))
            # Populate the file preview tree
            self.populate_file_tree()
        else:
            self.logger.info("No music zip files found")
            self.show_error("No music zip files found")
            self.extract_button.config(state=tk.DISABLED, style='Disabled.TButton')
            self.update_statistics(found=0)
            # Clear the file tree
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
            
    def find_music_zips(self):
        """Find all zip files matching the pattern in Downloads folder"""
        if not os.path.exists(self.downloads_folder):
            self.logger.error(f"Downloads folder not found: {self.downloads_folder}")
            return []
        
        music_zips = []
        for file in os.listdir(self.downloads_folder):
            if file.lower().endswith('.zip'):
                match = re.match(self.zip_pattern, file, re.IGNORECASE)
                if match:
                    artist_name = match.group(1).strip()
                    album_name = match.group(2).strip()
                    zip_path = os.path.join(self.downloads_folder, file)
                    music_zips.append({
                        'zip_path': zip_path,
                        'filename': file,
                        'artist': artist_name,
                        'album': album_name
                    })
                    self.logger.info(f"Found: {file} -> Artist: '{artist_name}', Album: '{album_name}'")
        
        return music_zips
        
    def extract_all(self):
        """Extract all found music zip files"""
        if not self.music_zips:
            self.show_error("No music zip files found. Please scan first.")
            messagebox.showwarning("No Files", "No music zip files found. Please scan first.")
            return
            
        self.show_processing("Starting extraction process...")
        # Show loading dialog
        self.show_extraction_loading()
        # Run extraction in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._extract_all_thread)
        thread.daemon = True
        thread.start()
        
    def _extract_all_thread(self):
        """Extract all files in a separate thread"""
        self.extract_button.config(state=tk.DISABLED, style='Disabled.TButton')
        self.scan_button.config(state=tk.DISABLED)
        
        try:
            # Ensure music library exists
            self.ensure_music_library_exists()
            
            total_files = len(self.music_zips)
            processed = 0
            failed = 0
            
            for i, zip_info in enumerate(self.music_zips):
                progress_percent = (i / total_files) * 100
                self.progress_var.set(progress_percent)
                
                # Update status with current file being processed
                current_file = zip_info['filename']
                self.root.after(0, lambda f=current_file, p=progress_percent: 
                    self.show_processing(f"Processing {f} ({p:.1f}%)"))
                
                self.root.update_idletasks()
                
                if self.process_music_zip(zip_info):
                    processed += 1
                    self.logger.info(f"✓ Successfully processed: {current_file}")
                else:
                    failed += 1
                    self.logger.error(f"✗ Failed to process: {current_file}")
                    
                # Update statistics in real-time
                self.root.after(0, lambda p=processed, f=failed: 
                    self.update_statistics(processed=p, failed=f))
                    
            self.progress_var.set(100)
            self.logger.info(f"Processing complete. Successfully processed: {processed}, Failed: {failed}")
            
            # Update statistics
            self.root.after(0, lambda: self.update_statistics(
                found=len(self.music_zips), processed=processed, failed=failed))
            
            # Hide loading dialog and show completion message
            self.root.after(0, lambda: self.hide_extraction_loading())
            self.root.after(0, lambda: self.show_success_dialog(processed, failed, self.music_zips))
            self.root.after(0, lambda: self.show_success("Extraction completed successfully"))
                
        except Exception as e:
            self.logger.error(f"Error during extraction: {e}")
            self.root.after(0, lambda: self.hide_extraction_loading())
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error during extraction: {e}"))
            self.root.after(0, lambda: self.show_error("Extraction failed"))
            
        finally:
            self.extract_button.config(state=tk.NORMAL)
            self.scan_button.config(state=tk.NORMAL)
            self.progress_var.set(0)
            
    def ensure_music_library_exists(self):
        """Ensure the music library directory exists"""
        Path(self.music_library_path).mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Music library directory ensured: {self.music_library_path}")
        
    def extract_album_folder(self, zip_path):
        """Extract the album folder from the zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                album_folders = set()
                for file_path in file_list:
                    parts = file_path.split('/')
                    if len(parts) > 1 and parts[0]:
                        album_folders.add(parts[0])
                
                if len(album_folders) == 1:
                    album_folder_name = list(album_folders)[0]
                    self.logger.info(f"Found album folder in zip: {album_folder_name}")
                    return album_folder_name
                else:
                    self.logger.warning(f"Unexpected zip structure in {zip_path}. Found folders: {album_folders}")
                    return None
                    
        except zipfile.BadZipFile:
            self.logger.error(f"Bad zip file: {zip_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading zip file {zip_path}: {e}")
            return None
            
    def process_music_zip(self, zip_info):
        """Process a single music zip file"""
        zip_path = zip_info['zip_path']
        artist_name = zip_info['artist']
        album_name = zip_info['album']
        
        self.logger.info(f"Processing: {zip_info['filename']}")
        
        # Create artist directory - always organize as /Music/Artist/Album/
        artist_dir = os.path.join(self.music_library_path, artist_name)
        Path(artist_dir).mkdir(parents=True, exist_ok=True)
        
        # Extract album folder from zip
        album_folder_name = self.extract_album_folder(zip_path)
        if not album_folder_name:
            self.logger.error(f"Could not extract album folder from {zip_path}")
            return False
        
        # Create temporary extraction directory
        temp_dir = os.path.join(self.downloads_folder, f"temp_extract_{os.getpid()}")
        
        try:
            # Extract zip to temporary directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Source and destination paths
            # Output structure: /Music/Artist/Album/songs
            source_album_path = os.path.join(temp_dir, album_folder_name)
            dest_album_path = os.path.join(artist_dir, album_name)
            
            # Check if album already exists
            if os.path.exists(dest_album_path):
                self.logger.warning(f"Album already exists: {dest_album_path}")
                # In GUI mode, we'll overwrite by default
                if os.path.exists(dest_album_path):
                    shutil.rmtree(dest_album_path)
            
            # Move album folder to destination
            if os.path.exists(source_album_path):
                shutil.move(source_album_path, dest_album_path)
                self.logger.info(f"Successfully moved album to: {dest_album_path}")
            else:
                self.logger.error(f"Album folder not found after extraction: {source_album_path}")
                return False
            
            # Delete the zip file if auto_delete is enabled
            if self.auto_delete_var.get():
                os.remove(zip_path)
                self.logger.info(f"Deleted zip file: {zip_path}")
            else:
                self.logger.info(f"Kept zip file: {zip_path} (auto-delete disabled)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {zip_path}: {e}")
            return False
        
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

def main():
    """Main function to run the GUI application"""
    try:
        root = tk.Tk()
        app = MusicExtractorGUI(root)
        root.mainloop()
    except Exception as e:
        # Show error in a simple dialog if GUI fails to start
        import tkinter.messagebox as mb
        mb.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main() 
