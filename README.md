# SRT to Markdown Converter

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-3.0-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

Convert SRT subtitle files from online courses (Udemy, Coursera, etc.) **OR** YouTube video collections into clean Markdown documents for **NotebookLM**, **Custom GPT**, **Obsidian**, or any knowledge base.

## ✨ Features

### 🎓 Course Mode (Default)
- 🔄 **Batch Processing** - Convert all courses at once
- 📝 **Clean Extraction** - Removes timestamps & line numbers automatically
- 📂 **Structure Preservation** - Maintains course → section → lecture hierarchy
- 📊 **Auto Metadata** - Generates section/lecture/resource counts
- 📖 **Table of Contents** - Clickable navigation links with resource badges
- 🎯 **Custom Paths** - Flexible input/output folder configuration
- ⚡ **No Dependencies** - Pure Python standard library
- 🔍 **Recursive Scanning** - Supports unlimited folder depth (Coursera, LinkedIn Learning, etc.)

### 🎥 YouTube Mode (v3.0 - NEW!)
- 📹 **Video Collections** - Compile independent YouTube videos by topic
- 🤖 **Custom GPT Ready** - Perfect format for training AI assistants
- 👥 **Creator Detection** - Automatically extracts channel/creator names
- 📝 **Plain Text Support** - Works with `.srt` and `.txt` subtitle downloads
- 🔄 **Incremental Updates** - Re-run to add new videos to existing knowledge base
- 📊 **Collection Stats** - Video count, contributors, last updated

### 📦 v2.0: Resource Detection

Automatically detects and lists course resources per section:

| Type | Icon | Examples |
|------|------|----------|
| PDF | 📄 | Slides, cheatsheets, checklists |
| SQL | 🗃️ | Database scripts, solutions |
| ZIP | 📦 | Project files, templates |
| HTML | 🔗 | Quizzes, resource links |
| Excel/CSV | 📊 | Datasets, spreadsheets |
| Python | 🐍 | Script files |
| Jupyter | 📓 | Notebooks |

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/queery-id/srt-to-markdown.git
cd srt-to-markdown

# No dependencies needed - just Python 3.7+
```

## 🚀 Usage

### Interactive Mode (Easiest!)

Simply run the executable without any arguments:

```bash
# Double-click srt-to-markdown.exe or run:
python srt_to_markdown.py
```

You'll see a friendly menu:
```
============================================================
🎬 SRT to Markdown Converter v3.0
============================================================

Select Mode:
  1. Course Mode (Udemy, Coursera, LinkedIn Learning)
  2. YouTube Mode (Video Collections for Custom GPT)
  3. Exit

Enter choice (1-3):
```

### Course Mode

```bash
# Process all courses in default folder
python srt_to_markdown.py

# Custom input folder
python srt_to_markdown.py -i "D:/MyCourses"

# Custom output folder
python srt_to_markdown.py -o "D:/Output"

# Process single course
python srt_to_markdown.py -c "SQL Bootcamp"
```

### YouTube Mode

```bash
# Interactive (prompts for folder)
python srt_to_markdown.py --youtube

# Direct path
python srt_to_markdown.py --youtube -i "D:/YouTube/Claude Code"

# Output will be saved in the same folder as input
# Example: D:/YouTube/Claude Code/Claude Code.md
```

### Interactive Batch Runner (Windows)

```cmd
# Double-click or run:
run.bat
```

## 📁 Folder Structure

### Course Mode (Udeler, Coursera, etc.)
```
Input/
├── Course 1/
│   ├── Section 1/
│   │   ├── Lecture 1.srt
│   │   ├── Lecture 2.srt
│   │   └── slides.pdf
│   └── Section 2/
│       └── Lecture 3.srt
└── Course 2/
    └── ...

Output/
├── Course 1.md
└── Course 2.md
```

### YouTube Mode
```
Input/
└── Claude Code/              ← Topic folder
    ├── Video 1.srt
    ├── Video 2.txt
    └── Video 3.srt

Output (same folder):
└── Claude Code/
    ├── Claude Code.md        ← Generated KB
    ├── Video 1.srt
    ├── Video 2.txt
    └── Video 3.srt
```

## 📄 Output Format

### Course Mode Example
```markdown
# Course Name

## Course Information
- Total Sections: 5
- Total Lectures: 42
- Total Resources: 15
- Generated: 2024-01-01

## Table of Contents
1. [Section 1](#section-1) 📦 3 resources
2. [Section 2](#section-2)

## Section 1

### 📚 Section Resources
| File | Type | Description |
|------|------|-------------|
| 📄 slides.pdf | pdf | Lecture slides |

### 📝 Lecture Transcripts
#### Lecture 1
[Clean transcript content...]
```

### YouTube Mode Example
```markdown
# Claude Code - Knowledge Base

*YouTube Video Collection for Custom GPT*

## 📊 Collection Information
- **Topic:** Claude Code
- **Total Videos:** 5
- **Last Updated:** 2026-01-08
- **Contributors:** Creator A, Creator B

## 📑 Table of Contents
1. [Video Title 1](#1-video-title-1)
2. [Video Title 2](#2-video-title-2)

## 🎥 Video Transcripts

### 1. Video Title 1
**Creator:** Creator A
**Source:** `video1.srt`

#### Transcript
[Clean transcript content...]
```

## 🎯 Use Cases

### Course Mode
- 📚 **NotebookLM** - Create AI-powered study assistants
- 🧠 **Obsidian** - Build personal knowledge graphs
- 🔍 **Search** - Full-text search across all courses
- 📖 **Review** - Quick course content review
- 🎓 **Study Notes** - Convert lectures to readable notes

### YouTube Mode
- 🤖 **Custom GPT** - Train AI on specific topics
- 📚 **Knowledge Base** - Compile expert knowledge from multiple creators
- 🔍 **Research** - Aggregate information on specific subjects
- 📖 **Learning** - Create comprehensive topic guides
- 🎯 **Topic Mastery** - Combine best tutorials on one subject

## 🛠️ Advanced Features

- **Encoding Support**: UTF-8, Latin-1, CP1252
- **Natural Sorting**: "Section 2" before "Section 10"
- **Clean Names**: Removes numbering prefixes
- **Resource Descriptions**: Smart filename-based descriptions
- **Recursive Scanning**: Handles any folder depth
- **Creator Detection**: Extracts from filename patterns

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- **Repository**: https://github.com/queery-id/srt-to-markdown
- **Issues**: https://github.com/queery-id/srt-to-markdown/issues

---

Made with ❤️ for learners and knowledge builders
