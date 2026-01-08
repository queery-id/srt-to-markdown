#!/usr/bin/env python3
"""
SRT to Markdown Converter for NotebookLM
=========================================
Converts Udeler course SRT files into clean Markdown documents.
Now includes course resources (PDF, SQL, ZIP, etc.) for complete context.

Usage:
    python srt_to_markdown.py                           # Process default Udeler folder
    python srt_to_markdown.py -i "C:/path/to/courses"   # Custom input folder
    python srt_to_markdown.py -o "C:/path/to/output"    # Custom output folder
    python srt_to_markdown.py -c "Course Name"          # Process single course
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict


# Default paths
DEFAULT_INPUT = r"C:\Users\HYPE\Downloads\Udeler"
DEFAULT_OUTPUT = Path(__file__).parent / "output"

# Resource file extensions to detect
RESOURCE_EXTENSIONS = {
    'pdf': {'icon': '📄', 'category': 'Documentation', 'desc': 'PDF document'},
    'sql': {'icon': '🗃️', 'category': 'Database', 'desc': 'SQL script'},
    'zip': {'icon': '📦', 'category': 'Project Files', 'desc': 'Archive/project files'},
    'html': {'icon': '🔗', 'category': 'Links', 'desc': 'Web resource/quiz'},
    'xlsx': {'icon': '📊', 'category': 'Spreadsheet', 'desc': 'Excel spreadsheet'},
    'xls': {'icon': '📊', 'category': 'Spreadsheet', 'desc': 'Excel spreadsheet'},
    'csv': {'icon': '📊', 'category': 'Data', 'desc': 'CSV data file'},
    'json': {'icon': '📋', 'category': 'Data', 'desc': 'JSON data file'},
    'py': {'icon': '🐍', 'category': 'Code', 'desc': 'Python script'},
    'ipynb': {'icon': '📓', 'category': 'Code', 'desc': 'Jupyter notebook'},
    'txt': {'icon': '📝', 'category': 'Text', 'desc': 'Text file'},
    'docx': {'icon': '📄', 'category': 'Documentation', 'desc': 'Word document'},
    'pptx': {'icon': '📽️', 'category': 'Presentation', 'desc': 'PowerPoint presentation'},
}


def parse_srt_file(srt_path: Path) -> str:
    """
    Parse SRT file and extract clean text without timestamps.
    
    SRT format:
    1
    00:00:00,080 --> 00:00:02,920
    Hello and welcome to this course.
    
    2
    00:00:02,960 --> 00:00:06,680
    My name is John.
    """
    try:
        # Try UTF-8 first, then fall back to other encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(srt_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  ⚠️ Could not decode: {srt_path.name}")
            return ""
        
        # Remove BOM if present
        content = content.lstrip('\ufeff')
        
        # Pattern to match: number, timestamp line, and capture text
        # Split by double newline to get subtitle blocks
        blocks = re.split(r'\n\s*\n', content.strip())
        
        text_lines = []
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # Skip first line (number) and second line (timestamp)
                # Join the rest (actual subtitle text)
                text = ' '.join(lines[2:])
                text_lines.append(text.strip())
            elif len(lines) == 2:
                # Sometimes there's just number and timestamp with no text
                pass
        
        # Join all text with spaces, clean up multiple spaces
        full_text = ' '.join(text_lines)
        full_text = re.sub(r'\s+', ' ', full_text)
        
        return full_text.strip()
        
    except Exception as e:
        print(f"  ⚠️ Error parsing {srt_path.name}: {e}")
        return ""


def parse_plain_text(txt_path: Path) -> str:
    """
    Parse plain text transcript file (already cleaned, no timestamps).
    Common for YouTube subtitle downloads from services like GetSubs.cc
    """
    try:
        # Try UTF-8 first, then fall back to other encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(txt_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  ⚠️ Could not decode: {txt_path.name}")
            return ""
        
        # Remove BOM if present
        content = content.lstrip('\ufeff')
        
        # Clean up multiple spaces and newlines
        content = re.sub(r'\n\s*\n', '\n\n', content)  # Normalize paragraph breaks
        content = re.sub(r' +', ' ', content)  # Remove multiple spaces
        
        return content.strip()
        
    except Exception as e:
        print(f"  ⚠️ Error parsing {txt_path.name}: {e}")
        return ""


def natural_sort_key(s: str) -> List:
    """
    Sort strings with numbers naturally.
    "1. Intro", "2. Setup", "10. Advanced" instead of "1.", "10.", "2."
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]


def get_clean_name(name: str) -> str:
    """Remove leading numbers and dots from name."""
    # "1. Introduction to SQL" -> "Introduction to SQL"
    return re.sub(r'^\d+\.\s*', '', name)


def get_resource_description(filename: str) -> str:
    """Generate a descriptive label based on filename patterns."""
    name_lower = filename.lower()
    
    # Common patterns
    if 'solution' in name_lower:
        return "Solution/Answer key"
    elif 'project' in name_lower:
        return "Project files"
    elif 'quiz' in name_lower:
        return "Quiz/Assessment"
    elif 'resource' in name_lower or 'download' in name_lower:
        return "Downloadable resources"
    elif 'slide' in name_lower or 'presentation' in name_lower:
        return "Presentation slides"
    elif 'cheat' in name_lower or 'sheet' in name_lower:
        return "Cheat sheet/Reference"
    elif 'checklist' in name_lower:
        return "Checklist"
    elif 'template' in name_lower:
        return "Template"
    elif 'script' in name_lower:
        return "Script file"
    elif 'data' in name_lower or 'dataset' in name_lower:
        return "Dataset"
    elif 'bonus' in name_lower:
        return "Bonus content"
    elif 'read' in name_lower and 'me' in name_lower:
        return "Important notes"
    elif 'create' in name_lower or 'setup' in name_lower or 'install' in name_lower:
        return "Setup/Installation"
    
    return None


def scan_resources(section_dir: Path) -> List[Dict]:
    """Scan a section directory for resource files (non-SRT files)."""
    resources = []
    
    for file_path in section_dir.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower().lstrip('.')
            
            # Skip SRT files (handled separately)
            if ext == 'srt':
                continue
            
            # Check if it's a recognized resource type
            if ext in RESOURCE_EXTENSIONS:
                res_info = RESOURCE_EXTENSIONS[ext]
                
                # Generate description
                custom_desc = get_resource_description(file_path.stem)
                description = custom_desc if custom_desc else res_info['desc']
                
                resources.append({
                    'name': file_path.name,
                    'extension': ext.upper(),
                    'icon': res_info['icon'],
                    'category': res_info['category'],
                    'description': description,
                    'size_kb': round(file_path.stat().st_size / 1024, 1)
                })
    
    # Sort resources by name
    resources.sort(key=lambda x: natural_sort_key(x['name']))
    
    return resources


def scan_course(course_path: Path) -> Tuple[str, List[dict], dict]:
    """
    Scan a course folder and return structured data.
    
    Supports any folder depth by recursively finding all SRT files.
    Works with: Udeler, Coursera, LinkedIn Learning, Udemy downloaded, etc.
    
    Returns:
        course_name: Name of the course
        sections: List of sections with lectures and resources
        metadata: Course statistics
    """
    course_name = course_path.name
    sections = []
    total_srt_files = 0
    total_resources = 0
    resource_summary = {}  # Count by category
    
    # Recursively find ALL SRT files in the course folder (any depth)
    all_srt_files = sorted(
        list(course_path.rglob("*.srt")),
        key=lambda x: natural_sort_key(str(x))
    )
    
    if not all_srt_files:
        return course_name, [], {'course_name': course_name, 'total_sections': 0, 
                                  'total_lectures': 0, 'total_resources': 0,
                                  'resource_summary': {}, 
                                  'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                  'source_path': str(course_path)}
    
    # Group SRT files by their parent folder
    # This creates sections based on the folder where SRT files are located
    folder_groups = {}
    for srt_file in all_srt_files:
        parent = srt_file.parent
        if parent not in folder_groups:
            folder_groups[parent] = []
        folder_groups[parent].append(srt_file)
    
    # Sort folders by their path
    sorted_folders = sorted(folder_groups.keys(), key=lambda x: natural_sort_key(str(x)))
    
    # Process each folder as a "section"
    for folder_path in sorted_folders:
        srt_files = folder_groups[folder_path]
        lectures = []
        
        # Generate section name from relative path
        try:
            rel_path = folder_path.relative_to(course_path)
            # Use the relative path parts as section name
            if str(rel_path) == '.':
                section_name = 'Course Content'
            else:
                # Join path parts with " → " for readability
                section_name = ' → '.join(rel_path.parts)
        except ValueError:
            section_name = folder_path.name
        
        # Process SRT files in this folder
        for srt_file in sorted(srt_files, key=lambda x: natural_sort_key(x.name)):
            lecture_name = srt_file.stem  # filename without extension
            content = parse_srt_file(srt_file)
            
            if content:
                lectures.append({
                    'name': lecture_name,
                    'clean_name': get_clean_name(lecture_name),
                    'content': content
                })
                total_srt_files += 1
        
        # Scan for resources in this folder
        resources = scan_resources(folder_path)
        total_resources += len(resources)
        
        # Update resource summary
        for res in resources:
            cat = res['category']
            resource_summary[cat] = resource_summary.get(cat, 0) + 1
        
        # Add section if it has content OR resources
        if lectures or resources:
            sections.append({
                'name': section_name,
                'clean_name': get_clean_name(section_name),
                'lectures': lectures,
                'resources': resources
            })
    
    metadata = {
        'course_name': course_name,
        'total_sections': len(sections),
        'total_lectures': total_srt_files,
        'total_resources': total_resources,
        'resource_summary': resource_summary,
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'source_path': str(course_path)
    }
    
    return course_name, sections, metadata


def generate_markdown(course_name: str, sections: List[dict], metadata: dict) -> str:
    """Generate Markdown content from course data."""
    
    lines = []
    
    # Title
    lines.append(f"# {course_name}")
    lines.append("")
    
    # Metadata section
    lines.append("## Course Information")
    lines.append("")
    lines.append(f"- **Sections:** {metadata['total_sections']}")
    lines.append(f"- **Lectures:** {metadata['total_lectures']}")
    lines.append(f"- **Resources:** {metadata['total_resources']} files")
    lines.append(f"- **Generated:** {metadata['generated_date']}")
    lines.append("")
    
    # Resource summary by category
    if metadata['resource_summary']:
        lines.append("### Available Resources")
        lines.append("")
        for category, count in sorted(metadata['resource_summary'].items()):
            lines.append(f"- {category}: {count} file(s)")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    for i, section in enumerate(sections, 1):
        section_anchor = section['clean_name'].lower().replace(' ', '-').replace('&', 'and')
        section_anchor = re.sub(r'[^a-z0-9\-]', '', section_anchor)
        res_count = len(section.get('resources', []))
        res_badge = f" 📎{res_count}" if res_count > 0 else ""
        lines.append(f"{i}. [{section['name']}](#{section_anchor}){res_badge}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Content sections
    for section in sections:
        lines.append(f"## {section['name']}")
        lines.append("")
        
        # Show resources for this section FIRST (important for context)
        resources = section.get('resources', [])
        if resources:
            lines.append("### 📚 Section Resources")
            lines.append("")
            lines.append("| File | Type | Description |")
            lines.append("|------|------|-------------|")
            for res in resources:
                size_str = f" ({res['size_kb']} KB)" if res['size_kb'] > 100 else ""
                lines.append(f"| {res['icon']} {res['name']} | {res['extension']} | {res['description']}{size_str} |")
            lines.append("")
        
        # Then show transcript content
        if section['lectures']:
            lines.append("### 📝 Lecture Transcripts")
            lines.append("")
            
            for lecture in section['lectures']:
                lines.append(f"#### {lecture['name']}")
                lines.append("")
                lines.append(lecture['content'])
                lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)


def process_course(course_path: Path, output_dir: Path) -> Optional[Path]:
    """Process a single course and save Markdown file."""
    
    print(f"\n📚 Processing: {course_path.name}")
    
    course_name, sections, metadata = scan_course(course_path)
    
    if not sections:
        print(f"  ⚠️ No content found, skipping...")
        return None
    
    print(f"  📂 Found {metadata['total_sections']} sections, {metadata['total_lectures']} lectures, {metadata['total_resources']} resources")
    
    # Generate Markdown
    markdown_content = generate_markdown(course_name, sections, metadata)
    
    # Save to file
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean filename (remove invalid characters)
    safe_name = re.sub(r'[<>:"/\\|?*]', '', course_name)
    output_file = output_dir / f"{safe_name}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"  ✅ Saved: {output_file.name}")
    
    return output_file


def scan_youtube_collection(folder_path: Path) -> Tuple[str, List[dict], dict]:
    """
    Scan a YouTube video collection folder (flat SRT/TXT files).
    
    Returns:
        topic_name: Name of the topic/collection
        videos: List of video transcripts
        metadata: Collection statistics
    """
    topic_name = folder_path.name
    videos = []
    
    # Find all SRT and TXT files directly in this folder
    srt_files = sorted(
        list(folder_path.glob("*.srt")) + list(folder_path.glob("*.txt")),
        key=lambda x: natural_sort_key(x.name)
    )
    
    if not srt_files:
        return topic_name, [], {
            'topic_name': topic_name,
            'total_videos': 0,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'source_path': str(folder_path)
        }
    
    # Process each SRT/TXT file as a video
    for srt_file in srt_files:
        video_title = srt_file.stem
        
        # Use appropriate parser based on file extension
        if srt_file.suffix.lower() == '.srt':
            content = parse_srt_file(srt_file)
        else:  # .txt or other
            content = parse_plain_text(srt_file)
        
        if content:
            # Extract potential creator from filename
            # Common patterns: "Creator - Title", "Title [Creator]", etc.
            creator = "Unknown"
            if " - " in video_title:
                parts = video_title.split(" - ", 1)
                creator = parts[0].strip()
            elif "[" in video_title and "]" in video_title:
                match = re.search(r'\[([^\]]+)\]', video_title)
                if match:
                    creator = match.group(1).strip()
            
            videos.append({
                'title': video_title,
                'creator': creator,
                'content': content,
                'filename': srt_file.name
            })
    
    metadata = {
        'topic_name': topic_name,
        'total_videos': len(videos),
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'source_path': str(folder_path)
    }
    
    return topic_name, videos, metadata


def generate_youtube_markdown(topic_name: str, videos: List[dict], metadata: dict) -> str:
    """Generate Markdown content for YouTube video collection."""
    
    lines = []
    
    # Header
    lines.append(f"# {topic_name} - Knowledge Base")
    lines.append("")
    lines.append("*YouTube Video Collection for Custom GPT*")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Collection Info
    lines.append("## 📊 Collection Information")
    lines.append("")
    lines.append(f"- **Topic:** {metadata['topic_name']}")
    lines.append(f"- **Total Videos:** {metadata['total_videos']}")
    lines.append(f"- **Last Updated:** {metadata['last_updated']}")
    lines.append(f"- **Generated:** {metadata['generated_date']}")
    lines.append("")
    
    # Extract unique creators
    creators = set(v['creator'] for v in videos if v['creator'] != 'Unknown')
    if creators:
        lines.append(f"- **Contributors:** {', '.join(sorted(creators))}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Table of Contents
    lines.append("## 📑 Table of Contents")
    lines.append("")
    for idx, video in enumerate(videos, 1):
        lines.append(f"{idx}. [{video['title']}](#{idx}-{video['title'].lower().replace(' ', '-')})")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Video Transcripts
    lines.append("## 🎥 Video Transcripts")
    lines.append("")
    
    for idx, video in enumerate(videos, 1):
        lines.append(f"### {idx}. {video['title']}")
        lines.append("")
        
        if video['creator'] != 'Unknown':
            lines.append(f"**Creator:** {video['creator']}  ")
        
        lines.append(f"**Source:** `{video['filename']}`")
        lines.append("")
        lines.append("#### Transcript")
        lines.append("")
        lines.append(video['content'])
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Footer
    lines.append("## 📝 Notes")
    lines.append("")
    lines.append("This knowledge base was automatically generated from YouTube video subtitles.")
    lines.append("Use this as a reference for Custom GPT or other AI assistants.")
    lines.append("")
    lines.append(f"*Generated on {metadata['generated_date']}*")
    
    return '\n'.join(lines)


def process_youtube_collection(folder_path: Path) -> Optional[Path]:
    """Process a single YouTube collection folder."""
    
    print(f"\n🎥 Processing: {folder_path.name}")
    
    # Scan collection
    topic_name, videos, metadata = scan_youtube_collection(folder_path)
    
    if not videos:
        print("  ⚠️ No SRT files found, skipping...")
        return None
    
    print(f"  📂 Found {metadata['total_videos']} videos")
    
    # Generate Markdown
    markdown_content = generate_youtube_markdown(topic_name, videos, metadata)
    
    # Save to same folder as input
    safe_name = re.sub(r'[<>:"/\\|?*]', '', topic_name)
    output_file = folder_path / f"{safe_name}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"  ✅ Saved: {output_file.name}")
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Convert SRT tutorial files to Markdown for NotebookLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Course Mode (default)
  python srt_to_markdown.py                              # Process all courses
  python srt_to_markdown.py -i "D:/MyCourses"            # Custom input folder
  python srt_to_markdown.py -o "D:/Output"               # Custom output folder  
  python srt_to_markdown.py -c "SQL Bootcamp"            # Single course only
  
  # YouTube Mode
  python srt_to_markdown.py --youtube -i "D:/YouTube/Claude Code"   # Process YouTube collection
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default=DEFAULT_INPUT,
        help=f'Input folder containing courses or YouTube collections (default: {DEFAULT_INPUT})'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=str(DEFAULT_OUTPUT),
        help=f'Output folder for Markdown files (default: {DEFAULT_OUTPUT})'
    )
    
    parser.add_argument(
        '-c', '--course',
        type=str,
        default=None,
        help='Process only a specific course (partial name match)'
    )
    
    parser.add_argument(
        '--youtube',
        action='store_true',
        help='YouTube mode: Process flat SRT collections as knowledge base'
    )
    
    args = parser.parse_args()
    
    # Interactive Mode - Show menu if no arguments provided
    if len(sys.argv) == 1:  # No arguments provided
        print("=" * 60)
        print("🎬 SRT to Markdown Converter v3.0")
        print("=" * 60)
        print("\nSelect Mode:")
        print("  1. Course Mode (Udemy, Coursera, LinkedIn Learning)")
        print("  2. YouTube Mode (Video Collections for Custom GPT)")
        print("  3. Exit")
        print()
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "3":
            print("\n👋 Goodbye!")
            return
        elif choice == "2":
            args.youtube = True
        elif choice != "1":
            print("\n❌ Invalid choice. Exiting.")
            return
        
        # Get input folder
        print("\n📂 Enter input folder path:")
        if args.youtube:
            print("   Example: C:\\Users\\HYPE\\Downloads\\Claude Code")
        else:
            print("   Example: C:\\Users\\HYPE\\Downloads\\Udeler")
        
        user_input = input("   Path (or press Enter for default): ").strip().strip('"')
        
        if user_input:
            args.input = user_input
        elif args.youtube:
            print("\n❌ Error: YouTube mode requires an input path")
            return
        
        print()
    
    # YouTube Mode
    if args.youtube:
        print("=" * 60)
        print("🎥 YouTube to Knowledge Base Converter v3.0")
        print("   For Custom GPT Training")
        print("=" * 60)
        
        input_path = Path(args.input)
        
        print(f"\n📁 Input:  {input_path}")
        
        if not input_path.exists():
            print(f"\n❌ Error: Input folder not found: {input_path}")
            return
        
        # Process the folder as a YouTube collection
        result = process_youtube_collection(input_path)
        
        if result:
            print("\n" + "=" * 60)
            print("✅ COMPLETE!")
            print("=" * 60)
            print(f"📄 Generated: {result.name}")
            print(f"📁 Location: {result.parent}")
        else:
            print("\n❌ No SRT files found in the folder")
        
        return
    
    # Course Mode - set paths
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    # Course Mode (default)
    print("=" * 60)
    print("🔄 SRT to Markdown Converter for NotebookLM v2.0")
    print("   Now with Resource Detection!")
    print("=" * 60)
    print(f"📁 Input:  {input_path}")
    print(f"📁 Output: {output_path}")
    
    if not input_path.exists():
        print(f"\n❌ Error: Input folder not found: {input_path}")
        return
    
    # Get list of courses (directories in input folder)
    courses = sorted(
        [d for d in input_path.iterdir() if d.is_dir()],
        key=lambda x: natural_sort_key(x.name)
    )
    
    # Filter by course name if specified
    if args.course:
        courses = [c for c in courses if args.course.lower() in c.name.lower()]
        if not courses:
            print(f"\n❌ No courses found matching: {args.course}")
            return
    
    print(f"\n📚 Found {len(courses)} course(s) to process")
    
    # Process each course
    processed = []
    total_resources = 0
    for course_path in courses:
        result = process_course(course_path, output_path)
        if result:
            processed.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ COMPLETE!")
    print("=" * 60)
    print(f"📊 Processed: {len(processed)} / {len(courses)} courses")
    print(f"📁 Output folder: {output_path}")
    
    if processed:
        print("\n📄 Generated files:")
        for f in processed:
            print(f"   - {f.name}")


if __name__ == "__main__":
    main()
