# 📍 QUICK START - SRT to Markdown Converter GUI

## 🎯 **Lokasi Aplikasi**

### **Folder Utama**
```
C:\Users\HYPE\Documents\Data D\Workspace\data-analytics-project\projects\srt-to-markdown\
```

### **Files Penting**

| File | Fungsi |
|------|--------|
| **`run-gui.bat`** | ⭐ **KLIK INI UNTUK MENJALANKAN GUI** |
| `srt_gui.py` | Source code GUI |
| `srt_to_markdown.py` | Source code CLI |
| `build-gui-exe.bat` | Build executable (.exe) |
| `GUI_GUIDE.md` | Dokumentasi lengkap GUI |
| `README.md` | Dokumentasi utama |

---

## 🚀 **Cara Menjalankan GUI**

### **Method 1: Double-Click** (Paling Mudah!)

1. **Buka folder:**
   ```
   C:\Users\HYPE\Documents\Data D\Workspace\data-analytics-project\projects\srt-to-markdown\
   ```

2. **Double-click file:**
   ```
   run-gui.bat
   ```

3. **GUI akan terbuka!** 🎉

---

### **Method 2: Command Line**

```bash
cd "C:\Users\HYPE\Documents\Data D\Workspace\data-analytics-project\projects\srt-to-markdown"
python srt_gui.py
```

---

## 🎨 **Cara Menggunakan GUI**

### **Step 1: Pilih Mode**
- **Course Mode** - Untuk Udemy, Coursera, LinkedIn Learning
- **YouTube Mode** - Untuk video collections

### **Step 2: Pilih Input Folder**
- Klik tombol **"Browse Folder"** di bagian Input Folder
- Pilih folder yang berisi file SRT

### **Step 3: Pilih Output Folder** (Course Mode saja)
- Klik tombol **"Browse Folder"** di bagian Output Folder
- Atau biarkan default (folder `output/`)

### **Step 4: Convert!**
- Klik tombol **"Convert"**
- Lihat progress bar dan activity log
- Done! ✅

---

## 📦 **Build Executable (.exe)**

Jika ingin membuat file `.exe` yang bisa dijalankan tanpa Python:

### **Step 1: Run Build Script**
```bash
build-gui-exe.bat
```

### **Step 2: Executable Location**
```
dist\SRT-Converter-GUI.exe
```

### **Step 3: Distribute**
Copy file `.exe` ke komputer lain dan jalankan!

**File Size:** ~15-20 MB (includes all dependencies)

---

## 🎯 **Example Use Cases**

### **Convert Udemy Course**
1. Run GUI: `run-gui.bat`
2. Select: **Course Mode**
3. Input: `C:\Downloads\Udemy\SQL Bootcamp`
4. Output: `C:\Documents\Converted`
5. Click: **Convert**
6. Result: `SQL Bootcamp.md` in output folder

### **Convert YouTube Collection**
1. Run GUI: `run-gui.bat`
2. Select: **YouTube Mode**
3. Input: `C:\Downloads\YouTube\Claude Code`
4. Click: **Convert**
5. Result: `Claude Code.md` in same folder

---

## 🔧 **Troubleshooting**

### **Problem: "ModuleNotFoundError: No module named 'customtkinter'"**

**Solution:**
```bash
pip install -r requirements-gui.txt
```

### **Problem: GUI tidak muncul**

**Solution:**
1. Check Python version: `python --version` (harus 3.7+)
2. Reinstall dependencies: `pip install -r requirements-gui.txt`
3. Run dari command line untuk lihat error: `python srt_gui.py`

### **Problem: "No SRT files found"**

**Solution:**
- Pastikan folder input berisi file `.srt` atau `.txt`
- Check folder structure sesuai mode yang dipilih

---

## 📚 **Documentation**

| File | Isi |
|------|-----|
| `GUI_GUIDE.md` | Panduan lengkap GUI |
| `GUI_COMPLETE.md` | Summary implementasi |
| `README.md` | Dokumentasi utama |
| `UPDATE_v3.0.2.md` | Update terbaru |

---

## 🎊 **Quick Reference**

### **Keyboard Shortcuts**
- **Alt+F4** - Close GUI
- **Ctrl+C** - Copy dari log
- **Ctrl+A** - Select all di log

### **Theme Toggle**
- Klik switch **"🌙 Dark Mode"** di footer
- Toggle antara Dark/Light mode

### **Clear Log**
- Klik tombol **"Clear Log"** di footer
- Bersihkan activity log

---

## 📞 **Need Help?**

1. **Read Documentation:**
   - `GUI_GUIDE.md` - Comprehensive guide
   - `README.md` - Main documentation

2. **Check Examples:**
   - Lihat folder `Input/` untuk contoh struktur

3. **Test with Sample:**
   - Gunakan folder test untuk coba fitur

---

**🎉 SELAMAT MENGGUNAKAN!**

*SRT to Markdown Converter v3.0.2 + GUI v1.0*
*Built with ❤️ using CustomTkinter*
