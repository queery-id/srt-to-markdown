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
    
    Supports two folder structures:
    1. Hierarchical: Course → Section folders → .srt files
    2. Flat: Course → .srt files directly (no section subfolders)
    
    Returns:
        course_name: Name of the course
        sections: List of sections with lectures and resources
        metadata: Course statistics
    """
    course_name = course_path.name
    sections = []
    total_lectures = 0
    total_srt_files = 0
    total_resources = 0
    resource_summary = {}  # Count by category
    
    # Check if there are SRT files directly in the course folder (flat structure)
    root_srt_files = sorted(
        list(course_path.glob("*.srt")),
        key=lambda x: natural_sort_key(x.name)
    )
    
    # Get all subdirectories (potential sections)
    section_dirs = sorted(
        [d for d in course_path.iterdir() if d.is_dir()],
        key=lambda x: natural_sort_key(x.name)
    )
    
    # If there are SRT files in root, treat them as a single "Main Content" section
    if root_srt_files:
        lectures = []
        
        for srt_file in root_srt_files:
            lecture_name = srt_file.stem  # filename without extension
            content = parse_srt_file(srt_file)
            
            if content:
                lectures.append({
                    'name': lecture_name,
                    'clean_name': get_clean_name(lecture_name),
                    'content': content
                })
                total_srt_files += 1
            
            total_lectures += 1
        
        # Scan for resources in course root
        resources = scan_resources(course_path)
        total_resources += len(resources)
        
        # Update resource summary
        for res in resources:
            cat = res['category']
            resource_summary[cat] = resource_summary.get(cat, 0) + 1
        
        if lectures or resources:
            sections.append({
                'name': 'Course Content',
                'clean_name': 'Course Content',
                'lectures': lectures,
                'resources': resources
            })
    
    # Process subdirectories (sections)
    for section_dir in section_dirs:
        section_name = section_dir.name
        lectures = []
        
        # Get all SRT files in this section
        srt_files = sorted(
            list(section_dir.glob("*.srt")),
            key=lambda x: natural_sort_key(x.name)
        )
        
        for srt_file in srt_files:
            lecture_name = srt_file.stem  # filename without extension
            content = parse_srt_file(srt_file)
            
            if content:
                lectures.append({
                    'name': lecture_name,
                    'clean_name': get_clean_name(lecture_name),
                    'content': content
                })
                total_srt_files += 1
            
            total_lectures += 1
        
        # Scan for resources in this section
        resources = scan_resources(section_dir)
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


def main():
    parser = argparse.ArgumentParser(
        description="Convert SRT tutorial files to Markdown for NotebookLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python srt_to_markdown.py                              # Process all courses
  python srt_to_markdown.py -i "D:/MyCourses"            # Custom input folder
  python srt_to_markdown.py -o "D:/Output"               # Custom output folder  
  python srt_to_markdown.py -c "SQL Bootcamp"            # Single course only
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default=DEFAULT_INPUT,
        help=f'Input folder containing courses (default: {DEFAULT_INPUT})'
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
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
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
