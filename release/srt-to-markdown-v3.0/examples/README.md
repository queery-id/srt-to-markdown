# Examples

## Course Mode Example

Place your course folders in `course-mode/` folder:

```
course-mode/
└── SQL Bootcamp/
    ├── Section 1/
    │   ├── 1. Introduction.srt
    │   └── 2. Setup.srt
    └── Section 2/
        └── 1. Queries.srt
```

Then run:
```
srt-to-markdown.exe -i "examples\course-mode"
```

## YouTube Mode Example

Place your video subtitles in `youtube-mode/` folder:

```
youtube-mode/
└── Claude Code/
    ├── video1.srt
    ├── video2.txt
    └── video3.srt
```

Then run:
```
srt-to-markdown.exe --youtube -i "examples\youtube-mode\Claude Code"
```
