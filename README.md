# SRT to Markdown Converter

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

Convert SRT subtitle files from online courses (Udemy, Coursera, etc.) into clean Markdown documents for **NotebookLM**, **Obsidian**, or any knowledge base.

## ✨ Features

- 🔄 **Batch Processing** - Convert all courses at once
- 📝 **Clean Extraction** - Removes timestamps & line numbers automatically
- 📂 **Structure Preservation** - Maintains course → section → lecture hierarchy
- 📊 **Auto Metadata** - Generates section/lecture/resource counts
- 📖 **Table of Contents** - Clickable navigation links with resource badges
- 🎯 **Custom Paths** - Flexible input/output folder configuration
- ⚡ **No Dependencies** - Pure Python standard library

### 🆕 v2.0: Resource Detection

Automatically detects and lists course resources per section:

| Type | Icon | Examples |
|------|------|----------|
| PDF | � | Slides, cheatsheets, checklists |
| SQL | 🗃️ | Database scripts, solutions |
| ZIP | �📦 | Project files, templates |
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

```bash
# Process all courses in default folder
python srt_to_markdown.py

# Custom input folder
python srt_to_markdown.py -i "/path/to/courses"

# Custom output folder
python srt_to_markdown.py -o "/path/to/output"

# Process single course (partial name match)
python srt_to_markdown.py -c "SQL Bootcamp"

# Combine options
python srt_to_markdown.py -i "/courses" -o "/output" -c "Python"
```

## 📁 Expected Input Structure

```
courses/
├── Course Name 1/
│   ├── 1. Section Name/
│   │   ├── 1. Lecture.srt
│   │   ├── 2. Lecture.srt
│   │   ├── resources.pdf      # ← Auto-detected
│   │   ├── project.zip        # ← Auto-detected
│   │   └── ...
│   ├── 2. Section Name/
│   │   └── ...
│   └── ...
├── Course Name 2/
│   └── ...
```

## 📄 Output Format

```markdown
# Course Name

## Course Information
- **Sections:** 28
- **Lectures:** 291
- **Resources:** 45 files

### Available Resources
- Documentation: 12 file(s)
- Database: 8 file(s)
- Project Files: 5 file(s)

---

## Table of Contents
1. Introduction 📎3
2. Getting Started 📎5
...

---

## 1. Introduction

### 📚 Section Resources
| File | Type | Description |
|------|------|-------------|
| 📦 sql-project.zip | ZIP | Project files |
| 📄 slides.pdf | PDF | Presentation slides |
| 🗃️ setup.sql | SQL | Setup/Installation |

### 📝 Lecture Transcripts

#### 1. Welcome
Hello and welcome to this course...

#### 2. Course Overview
In this section we will cover...
```

## 🎯 Use Cases

- **NotebookLM** - Upload markdown files as sources for AI-powered Q&A
- **Obsidian** - Build a searchable knowledge base from courses
- **Custom GPT** - Create training data for course-specific assistants (with full resource context!)
- **Study Notes** - Quick reference for course content and materials

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
