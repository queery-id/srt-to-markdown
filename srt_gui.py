#!/usr/bin/env python3
"""
SRT to Markdown Converter GUI - Modern interface using CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
import queue

# Import the main converter functions
from srt_to_markdown import process_course, process_youtube_collection

# Set appearance
ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"


class SRTConverterGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🎬 SRT to Markdown Converter")
        self.window.geometry("900x700")
        
        # Center window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Variables
        self.is_processing = False
        self.log_queue = queue.Queue()
        self.mode = ctk.StringVar(value="course")  # "course" or "youtube"
        self.input_folder = None
        self.output_folder = None
        
        # Create UI
        self.create_ui()
        
        # Start log update checker
        self.check_log_queue()
        
    def create_ui(self):
        """Create the user interface"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ========== HEADER ==========
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎬 SRT to Markdown Converter",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Convert subtitle files to knowledge base format",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # ========== MODE SELECTION ==========
        mode_frame = ctk.CTkFrame(main_frame)
        mode_frame.pack(fill="x", pady=(0, 15))
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="📁 Mode Selection",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        mode_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Radio buttons
        radio_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.course_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Course Mode (Udemy, Coursera, LinkedIn Learning)",
            variable=self.mode,
            value="course",
            command=self.on_mode_change,
            font=ctk.CTkFont(size=13)
        )
        self.course_radio.pack(side="left", padx=(0, 20))
        
        self.youtube_radio = ctk.CTkRadioButton(
            radio_frame,
            text="YouTube Mode (Video Collections for Custom GPT)",
            variable=self.mode,
            value="youtube",
            command=self.on_mode_change,
            font=ctk.CTkFont(size=13)
        )
        self.youtube_radio.pack(side="left")
        
        # ========== INPUT FOLDER ==========
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", pady=(0, 15))
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="📂 Input Folder",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Folder selection
        folder_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        folder_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.input_label = ctk.CTkLabel(
            folder_frame,
            text="No folder selected",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.input_label.pack(side="left", fill="x", expand=True)
        
        browse_input_btn = ctk.CTkButton(
            folder_frame,
            text="Browse Folder",
            command=self.browse_input,
            width=140,
            height=35
        )
        browse_input_btn.pack(side="right", padx=(10, 0))
        
        # ========== OUTPUT FOLDER (Course Mode only) ==========
        self.output_frame = ctk.CTkFrame(main_frame)
        self.output_frame.pack(fill="x", pady=(0, 15))
        
        output_label = ctk.CTkLabel(
            self.output_frame,
            text="📁 Output Folder (Course Mode only)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        output_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Output folder selection
        output_folder_frame = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        output_folder_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.output_label = ctk.CTkLabel(
            output_folder_frame,
            text="Default: output/ folder",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.output_label.pack(side="left", fill="x", expand=True)
        
        browse_output_btn = ctk.CTkButton(
            output_folder_frame,
            text="Browse Folder",
            command=self.browse_output,
            width=140,
            height=35
        )
        browse_output_btn.pack(side="right", padx=(10, 0))
        
        # ========== CONVERT BUTTON ==========
        self.convert_btn = ctk.CTkButton(
            main_frame,
            text="Convert",
            command=self.start_conversion,
            width=200,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            state="disabled"
        )
        self.convert_btn.pack(pady=(0, 15))
        
        # ========== PROGRESS SECTION ==========
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=(0, 15))
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="📊 Progress",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        progress_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 10))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to convert",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(padx=15, pady=(0, 15))
        
        # ========== LOG SECTION ==========
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True)
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="📋 Activity Log",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        log_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=150,
            font=ctk.CTkFont(size=11, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # ========== FOOTER ==========
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            footer_frame,
            text="🌙 Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(side="left")
        self.theme_switch.select()  # Default to dark mode
        
        # Clear log button
        clear_btn = ctk.CTkButton(
            footer_frame,
            text="Clear Log",
            command=self.clear_log,
            width=100,
            height=30
        )
        clear_btn.pack(side="right")
        
    def on_mode_change(self):
        """Handle mode change"""
        if self.mode.get() == "youtube":
            self.output_frame.pack_forget()
            self.log("📺 Switched to YouTube Mode")
        else:
            self.output_frame.pack(fill="x", pady=(0, 15), before=self.convert_btn)
            self.log("📚 Switched to Course Mode")
    
    def browse_input(self):
        """Browse for input folder"""
        folder = filedialog.askdirectory(title="Select Input Folder")
        
        if folder:
            self.input_folder = Path(folder)
            self.input_label.configure(text=os.path.basename(folder))
            self.convert_btn.configure(state="normal")
            self.log(f"✅ Selected input folder: {folder}")
    
    def browse_output(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        
        if folder:
            self.output_folder = Path(folder)
            self.output_label.configure(text=os.path.basename(folder))
            self.log(f"✅ Selected output folder: {folder}")
    
    def log(self, message):
        """Add message to log queue (thread-safe)"""
        self.log_queue.put(message)
        
    def check_log_queue(self):
        """Check for new log messages and update UI"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert("end", f"{message}\n")
                self.log_text.see("end")
        except queue.Empty:
            pass
        
        # Schedule next check
        self.window.after(100, self.check_log_queue)
        
    def clear_log(self):
        """Clear the log textbox"""
        self.log_text.delete("1.0", "end")
        
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def start_conversion(self):
        """Start conversion process"""
        if not self.input_folder:
            messagebox.showwarning("Warning", "Please select an input folder!")
            return
        
        if self.is_processing:
            messagebox.showwarning("Warning", "Conversion already in progress!")
            return
        
        # Start conversion in thread
        thread = threading.Thread(target=self._conversion_thread)
        thread.daemon = True
        thread.start()
    
    def _conversion_thread(self):
        """Run conversion in background thread"""
        self.is_processing = True
        self.convert_btn.configure(state="disabled")
        self.progress_bar.set(0)
        
        try:
            mode = self.mode.get()
            
            self.log(f"\n{'='*60}")
            self.log(f"🚀 Starting conversion in {mode.upper()} mode")
            self.log(f"{'='*60}\n")
            
            if mode == "youtube":
                self._process_youtube()
            else:
                self._process_course()
            
            self.log(f"\n{'='*60}")
            self.log("✅ Conversion completed successfully!")
            self.log(f"{'='*60}\n")
            
            self.status_label.configure(text="Conversion completed!")
            self.progress_bar.set(1.0)
            messagebox.showinfo("Success", "Conversion completed successfully!")
            
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            self.status_label.configure(text="Error occurred!")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            
        finally:
            self.is_processing = False
            self.convert_btn.configure(state="normal")
            self.progress_bar.set(0)
    
    def _process_youtube(self):
        """Process YouTube collection"""
        self.status_label.configure(text="Processing YouTube collection...")
        self.progress_bar.set(0.3)
        
        self.log(f"📂 Processing folder: {self.input_folder}")
        
        # Use the existing function
        result = process_youtube_collection(self.input_folder)
        
        self.progress_bar.set(0.9)
        
        if result:
            self.log(f"📄 Generated: {result.name}")
            self.log(f"📁 Location: {result.parent}")
        else:
            raise Exception("No SRT files found in the folder")
    
    def _process_course(self):
        """Process course folder"""
        self.status_label.configure(text="Processing course...")
        self.progress_bar.set(0.2)
        
        # Set output folder
        if self.output_folder:
            output_path = self.output_folder
        else:
            output_path = Path(__file__).parent / "output"
            output_path.mkdir(exist_ok=True)
        
        self.log(f"📂 Processing course: {self.input_folder.name}")
        
        # Use the existing function
        result = process_course(self.input_folder, output_path)
        
        self.progress_bar.set(0.9)
        
        if result:
            self.log(f"📄 Generated: {result.name}")
            self.log(f"📁 Location: {result.parent}")
        else:
            raise Exception("Failed to process course")
    
    def run(self):
        """Run the application"""
        self.log("🎬 SRT to Markdown Converter GUI started")
        self.log("Ready to convert subtitle files\n")
        self.window.mainloop()


def main():
    app = SRTConverterGUI()
    app.run()


if __name__ == "__main__":
    main()
