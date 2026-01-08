# 🧪 Testing Guide - YouTube Mode

## Quick Start Testing

### Method 1: Interactive Mode (Recommended for Testing)

1. **Run script tanpa argument:**
   ```bash
   python srt_to_markdown.py --youtube
   ```

2. **Script akan meminta input folder:**
   ```
   📂 Enter input folder path (folder containing video subtitle files):
      Example: C:\Users\HYPE\Downloads\Claude Code
      Path: _
   ```

3. **Paste path folder yang berisi subtitle files:**
   - Bisa dari Downloads
   - Bisa dari folder manapun
   - Support path dengan spasi
   - Otomatis remove quotes jika copy-paste dari explorer

4. **Output akan tersimpan di folder yang sama dengan input**

---

### Method 2: Direct Command Line

```bash
# Langsung specify input folder
python srt_to_markdown.py --youtube -i "C:\Users\HYPE\Downloads\Claude Code"
```

---

## 📁 Prepare Test Files

### Step 1: Organize by Topic

Buat folder berdasarkan topik, contoh:

```
Downloads/
├── Claude Code/
│   ├── video1.txt
│   ├── video2.txt
│   └── video3.txt
├── Power BI MCP/
│   ├── video1.txt
│   └── video2.txt
└── AI Productivity/
    └── video1.txt
```

### Step 2: Move Files from Downloads

**Option A: Manual (File Explorer)**
1. Buat folder baru di Downloads (misal: "Claude Code")
2. Drag & drop file subtitle ke folder tersebut
3. Copy path folder (klik address bar → Ctrl+C)

**Option B: PowerShell Command**
```powershell
# Buat folder
New-Item -ItemType Directory -Path "C:\Users\HYPE\Downloads\Claude Code Test"

# Pindahkan file (contoh)
Move-Item "C:\Users\HYPE\Downloads\Claude Code*.txt" `
          "C:\Users\HYPE\Downloads\Claude Code Test\"
```

---

## ✅ Test Scenarios

### Test 1: Basic YouTube Mode
**Input:**
- Folder: `Downloads/Claude Code Test`
- Files: 3 video subtitle files (.txt atau .srt)

**Expected Output:**
- File: `Claude Code Test.md` di folder yang sama
- Contains: 3 video transcripts
- Metadata: video count, creators, timestamps

**Command:**
```bash
python srt_to_markdown.py --youtube -i "C:\Users\HYPE\Downloads\Claude Code Test"
```

---

### Test 2: Mixed File Types
**Input:**
- 2 files `.txt` (plain text)
- 1 file `.srt` (with timestamps)

**Expected:**
- All 3 files processed correctly
- Timestamps removed from .srt
- Plain text preserved from .txt

---

### Test 3: Creator Detection
**Input files dengan pattern:**
- `Creator Name - Video Title.txt`
- `Video Title [Creator Name].txt`
- `Video Title.txt` (no creator)

**Expected:**
- Creator extracted correctly
- "Unknown" for files without pattern

---

### Test 4: Re-run (Update Mode)
**Steps:**
1. Run pertama dengan 2 files
2. Add 1 file baru ke folder
3. Run lagi

**Expected:**
- File .md di-overwrite
- Sekarang contains 3 videos
- Timestamp "Last Updated" berubah

---

## 🐛 Common Issues & Solutions

### Issue 1: "No SRT files found"
**Cause:** Folder kosong atau file extension salah
**Solution:** 
- Check file extension (.srt atau .txt)
- Pastikan files ada di folder root, bukan subfolder

### Issue 2: Path not found
**Cause:** Path salah atau typo
**Solution:**
- Copy path dari File Explorer address bar
- Gunakan quotes jika ada spasi
- Check backslash vs forward slash

### Issue 3: Encoding error
**Cause:** File dengan encoding non-standard
**Solution:** Script sudah handle UTF-8, Latin-1, CP1252 otomatis

---

## 📊 Expected Output Format

```markdown
# Topic Name - Knowledge Base

## 📊 Collection Information
- **Topic:** Topic Name
- **Total Videos:** 3
- **Last Updated:** 2026-01-08 15:10
- **Contributors:** Creator A, Creator B, Unknown

## 📑 Table of Contents
1. [Video 1 Title](#1-video-1-title)
2. [Video 2 Title](#2-video-2-title)
3. [Video 3 Title](#3-video-3-title)

## 🎥 Video Transcripts

### 1. Video 1 Title
**Creator:** Creator A
**Source:** `video1.txt`

#### Transcript
[Full transcript content...]
```

---

## 🎯 Ready to Test?

**Current Status:**
- ✅ Interactive mode ready
- ✅ Support .srt and .txt files
- ✅ Creator detection enabled
- ✅ Metadata generation working

**Next Steps:**
1. Organize 3 test files into 1 folder
2. Run: `python srt_to_markdown.py --youtube`
3. Paste folder path when prompted
4. Check output .md file

**Need help?** Kasih tau:
- Folder path yang mau di-test
- Jumlah files
- File extensions (.srt atau .txt)
