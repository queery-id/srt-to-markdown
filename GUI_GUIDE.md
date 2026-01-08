# SRT to Markdown Converter - GUI Version 🎨

## 🎯 Overview

Modern graphical user interface (GUI) untuk SRT to Markdown Converter, dibangun menggunakan **CustomTkinter** framework yang sama dengan Suno Downloader.

---

## ✨ Features

### 🎨 Modern Design
- ✅ **Dark Mode** - Professional dark theme (default)
- ✅ **Light Mode** - Toggle untuk light theme
- ✅ **Clean Layout** - Organized sections dengan clear visual hierarchy
- ✅ **Responsive UI** - Smooth interactions dan transitions

### 📁 Mode Selection
- ✅ **Course Mode** - Untuk Udemy, Coursera, LinkedIn Learning
- ✅ **YouTube Mode** - Untuk video collections (Custom GPT)
- ✅ **Dynamic UI** - Output folder hanya muncul di Course Mode

### 🚀 Processing Features
- ✅ **Folder Browser** - Easy folder selection dengan dialog
- ✅ **Progress Bar** - Visual feedback saat processing
- ✅ **Activity Log** - Real-time status updates
- ✅ **Thread-Safe** - Processing di background thread
- ✅ **Error Handling** - User-friendly error messages

---

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements-gui.txt
```

**Dependencies:**
- `customtkinter>=5.2.0` - Modern UI framework
- `pillow>=10.0.0` - Image processing support

### 2. Run GUI

**Option A: Using Batch Script**
```bash
run-gui.bat
```

**Option B: Direct Python**
```bash
python srt_gui.py
```

---

## 🎮 How to Use

### Course Mode

1. **Select Mode**
   - Click "Course Mode" radio button

2. **Select Input Folder**
   - Click "Browse Folder" under Input Folder
   - Navigate to your course folder (e.g., `C:\Downloads\Udemy\SQL Bootcamp`)

3. **Select Output Folder (Optional)**
   - Click "Browse Folder" under Output Folder
   - Or leave default (`output/` folder)

4. **Convert**
   - Click "Convert" button
   - Watch progress bar and activity log
   - Done! File saved to output folder

### YouTube Mode

1. **Select Mode**
   - Click "YouTube Mode" radio button
   - Output folder section akan hilang

2. **Select Input Folder**
   - Click "Browse Folder"
   - Navigate to your YouTube collection folder

3. **Convert**
   - Click "Convert" button
   - File akan disimpan di folder yang sama dengan input

---

## 🎨 UI Components

### Header
```
🎬 SRT to Markdown Converter
Convert subtitle files to knowledge base format
```

### Mode Selection
```
📁 Mode Selection
○ Course Mode (Udemy, Coursera, LinkedIn Learning)
○ YouTube Mode (Video Collections for Custom GPT)
```

### Input/Output
```
📂 Input Folder
[Selected folder name]  [Browse Folder]

📁 Output Folder (Course Mode only)
[Selected folder name or Default: output/ folder]  [Browse Folder]
```

### Progress
```
📊 Progress
████████████████░░░░░░░░░░░░ 60%
Processing: SQL Bootcamp - Section 3
```

### Activity Log
```
📋 Activity Log
┌────────────────────────────────────────┐
│ 🎬 SRT to Markdown Converter GUI started│
│ Ready to convert subtitle files         │
│                                         │
│ ✅ Selected input folder: Claude Code   │
│ 📂 Processing folder: Claude Code       │
│ 📄 Generated: Claude Code.md            │
│ ✅ Conversion completed successfully!   │
└────────────────────────────────────────┘
```

### Footer
```
🌙 Dark Mode                    [Clear Log]
```

---

## 🔧 Technical Details

### Framework
- **CustomTkinter 5.2.0+** - Modern Tkinter wrapper
- **Threading** - Background processing
- **Queue** - Thread-safe logging

### Architecture

```python
SRTConverterGUI
├── __init__()          # Initialize window & variables
├── create_ui()         # Build UI components
├── browse_input()      # Folder selection dialog
├── browse_output()     # Output folder dialog
├── start_conversion()  # Main entry point
├── _conversion_thread()# Background processing
├── _process_youtube()  # YouTube mode handler
├── _process_course()   # Course mode handler
└── run()              # Start application
```

### Thread Safety
- ✅ **Queue-based logging** - Thread-safe message passing
- ✅ **Daemon threads** - Auto-cleanup on exit
- ✅ **UI updates** - Scheduled via `window.after()`

---

## 📊 Comparison: CLI vs GUI

| Feature | CLI Version | GUI Version |
|---------|------------|-------------|
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Visual Feedback** | Text only | Progress bar + Log |
| **Folder Selection** | Manual typing | Browse dialog |
| **Error Messages** | Console text | Message boxes |
| **Theme** | Terminal default | Dark/Light mode |
| **Multi-tasking** | Blocks terminal | Background thread |
| **File Size** | ~2 MB | ~5 MB |

---

## 🎯 Use Cases

### Perfect For:
- ✅ **Non-technical users** - No command line needed
- ✅ **Visual learners** - See progress in real-time
- ✅ **Batch processing** - Easy folder selection
- ✅ **Windows users** - Native-looking interface

### CLI Still Better For:
- ⚠️ **Automation** - Scripting and batch files
- ⚠️ **Remote servers** - No GUI available
- ⚠️ **Power users** - Faster for keyboard warriors
- ⚠️ **CI/CD** - Automated pipelines

---

## 🚀 Building Executable

### Using PyInstaller

```bash
pyinstaller --onefile --windowed --name "SRT-Converter-GUI" --icon=icon.ico srt_gui.py
```

**Options:**
- `--onefile` - Single executable file
- `--windowed` - No console window
- `--name` - Custom executable name
- `--icon` - Custom icon (optional)

**Output:**
- `dist/SRT-Converter-GUI.exe` - Standalone executable
- Size: ~15-20 MB (includes CustomTkinter)

---

## 🎨 Customization

### Change Theme Color

```python
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
```

### Change Window Size

```python
self.window.geometry("900x700")  # Width x Height
```

### Add Custom Fonts

```python
font=ctk.CTkFont(size=13, family="Arial", weight="bold")
```

---

## 🐛 Troubleshooting

### GUI Won't Start

**Problem:** `ModuleNotFoundError: No module named 'customtkinter'`

**Solution:**
```bash
pip install -r requirements-gui.txt
```

### Progress Bar Not Moving

**Problem:** UI freezes during processing

**Solution:** Already handled! Processing runs in background thread.

### Dark Mode Not Working

**Problem:** Theme doesn't change

**Solution:** Toggle the switch in footer, or set system theme:
```python
ctk.set_appearance_mode("System")  # Follow system theme
```

---

## 📝 Future Enhancements

### Planned Features
- [ ] **Drag & Drop** - Drag folders directly to window
- [ ] **Recent Folders** - Quick access to recent paths
- [ ] **Settings Panel** - Save preferences
- [ ] **Batch Mode** - Process multiple folders at once
- [ ] **Preview** - Preview markdown before saving
- [ ] **Custom Output Name** - Rename output file
- [ ] **File Association** - Double-click .srt to open GUI

---

## 🎉 Summary

**GUI Version Benefits:**
- ✅ **User-Friendly** - No command line knowledge needed
- ✅ **Visual Feedback** - See what's happening in real-time
- ✅ **Professional Look** - Modern dark mode interface
- ✅ **Error Handling** - Clear error messages with dialogs
- ✅ **Cross-Platform** - Works on Windows, Mac, Linux

**Perfect for:**
- 📚 Students converting course materials
- 🎥 Content creators organizing YouTube transcripts
- 📖 Researchers building knowledge bases
- 👥 Teams sharing converted files

---

**Built with ❤️ using CustomTkinter**

*Version: 1.0*
*Last Updated: 2026-01-08*
