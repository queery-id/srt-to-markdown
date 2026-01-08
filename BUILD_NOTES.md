# Build Notes for Portable .exe

## Reference Project
Benchmark dari: `C:\Users\HYPE\Documents\Data D\Workspace\app-development\desktop-apps\suno-downloader`

## Tools yang Digunakan di Suno Downloader
- **PyInstaller** - untuk compile Python → .exe
- **build-exe.bat** - batch script untuk build
- **Inno Setup** (optional) - untuk installer

## Langkah Build (Referensi dari Suno Downloader)

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Buat spec file atau gunakan command langsung
```bash
pyinstaller --onefile --windowed --name "SRT to Markdown" srt_to_markdown.py
```

### 3. Untuk GUI (jika nanti ditambahkan)
Lihat `suno_gui.py` sebagai referensi untuk:
- tkinter GUI
- File dialog
- Progress bar
- Error handling

## File yang Perlu Dibuat

### build-exe.bat
```batch
@echo off
echo Building SRT to Markdown Converter...
pyinstaller --onefile --console --name "srt-to-markdown" srt_to_markdown.py
echo Build complete! Check dist/ folder
pause
```

### Untuk GUI Version (Future)
- Buat `srt_gui.py` dengan tkinter
- Mode selector: Course / YouTube
- Folder picker
- Progress indicator
- Log output

## Distribution
- Portable .exe di `dist/` folder
- Tidak perlu Python terinstall
- Include README.txt dengan instruksi

## Testing Checklist
- [ ] Test di Windows 10/11
- [ ] Test dengan berbagai encoding (UTF-8, Latin-1)
- [ ] Test Course mode
- [ ] Test YouTube mode
- [ ] Test dengan path yang punya spasi
- [ ] Test dengan nama file special characters

## Notes
- Keep it simple - CLI first
- GUI optional untuk user awam
- Pastikan error messages jelas
- Include sample input/output di README
