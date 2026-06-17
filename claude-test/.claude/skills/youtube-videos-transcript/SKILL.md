---
name: youtube-videos-transcript
description: |
  Extract transcript text from a YouTube video and save it as a .txt file in the output folder.
  Use this skill whenever the user asks to get, download, extract, or create a transcript from a YouTube video, or mentions a YouTube video transcript.
  Also use this skill if the user provides a YouTube URL and wants a text transcript saved to a file.
  This skill now includes enhanced error handling, URL validation, improved filename generation, and detailed output confirmation.
compatibility:
  tools: [bash, webfetch, write]
  dependencies:
    - youtube-transcript-api (Python library)
    - yt-dlp (optional, for video metadata)
---

# YouTube Videos Transcript Skill

## Purpose
This skill extracts the transcript from a YouTube video and saves it as a `.txt` file in the `output` folder with enhanced error handling, URL validation, and detailed output confirmation.

## Workflow
1. Validate the provided YouTube URL to ensure it's a valid YouTube link.
2. Extract the video ID from the validated YouTube URL.
3. Use `youtube-transcript-api` to fetch the English transcript.
4. If no transcript is available, report a detailed error to the user and stop.
5. Retrieve the video title (via `yt-dlp` or a lightweight web fetch) to use in the filename.
6. Generate a sanitized filename with a formatted timestamp.
7. Save the transcript text to `output/<SanitizedVideoName>_<timestamp>.txt`.
8. Confirm the saved file path to the user with detailed information (file size, line count, etc.).

## Detailed Steps

### 1. Validate YouTube URL
Check that the provided URL is a valid YouTube URL format before proceeding.
Supports:
- Standard youtube.com/watch?v=VIDEO_ID URLs
- Shortened youtu.be/VIDEO_ID URLs
- Embedded youtube.com/embed/VIDEO_ID URLs

### 2. Extract Video ID
Given a validated YouTube URL, parse it to get the `v` query parameter or handle shortened `youtu.be` links.

Examples:
- `https://www.youtube.com/watch?v=AbCdEfGhIjK` → `AbCdEfGhIjK`
- `https://youtu.be/AbCdEfGhIjK` → `AbCdEfGhIjK`
- `https://www.youtube.com/embed/AbCdEfGhIjK` → `AbCdEfGhIjK`

### 3. Fetch Transcript
Use the `youtube-transcript-api` Python package to fetch the English transcript.

If the package is not installed, install it first:
```bash
pip install youtube-transcript-api
```

Script: `scripts/get_transcript.py`

### 4. Handle Missing Transcript
If the API raises an exception indicating no transcript is available, immediately report a detailed error to the user including the video ID and suggest possible reasons (no English transcript, video private, etc.) and do not proceed.

### 5. Get Video Title
Use `yt-dlp` (preferred) or a lightweight web fetch to get the video title.

If `yt-dlp` is not installed, install it first:
```bash
pip install yt-dlp
```

Then run:
```bash
yt-dlp --get-title <video_url>
```

Sanitize the title for use in a filename (remove/replace special characters).

### 6. Generate Filename
Filename format: `<SanitizedVideoName>_<timestamp>.txt`
- `timestamp`: use a `YYYY-MM-DD_HH-MM-SS` formatted time for readability.
- Save to: `output/<filename>`
- Ensure the `output` directory exists; create it if it doesn't.

### 7. Save Transcript
Write the transcript content to the generated filename in the output folder.

### 8. Confirm Output
After saving, tell the user:
- Full path to the saved file
- File size in bytes and human-readable format
- Number of lines in the transcript
- Approximate word count
- Success confirmation message

## Error Handling
- **Invalid URL**: Inform the user and ask for a valid YouTube link with examples of supported formats.
- **Network errors**: Retry up to 2 times with exponential backoff, then report failure.
- **No transcript available**: Inform the user that the video does not have an English transcript available, suggesting possible reasons (video might not have captions, captions might be disabled, or video might be region-restricted).
- **yt-dlp not found**: Provide clear installation instructions.
- **youtube-transcript-api not found**: Provide clear installation instructions.
- **File system errors**: Report issues with creating the output directory or writing the file.

## Scripts
- `scripts/get_transcript.py`: Python script to fetch the transcript with improved error handling.
- `scripts/get_title.py`: Python script to fetch and sanitize the video title with enhanced filename safety.
- `scripts/validate_url.py`: New script to validate YouTube URLs.

## Example Usage
User: "Get the transcript from https://www.youtube.com/watch?v=dQw4w9WgXcQ"
Agent:
  1. Validates URL: ✓ Valid YouTube URL
  2. Extracts video ID: dQw4w9WgXcQ
  3. Runs get_transcript.py → fetches transcript
  4. Runs get_title.py → gets "Rick Astley - Never Gonna Give You Up (Official Music Video)"
  5. Sanitizes title → "Rick_Astley_-_Never_Gonna_Give_You_Up_Official_Music_Video"
  6. Generates filename with timestamp → Rick_Astley_-_Never_Gonna_Give_You_Up_Official_Music_Video_2026-06-07_14-30-22.txt
  7. Saves to: output/Rick_Astley_-_Never_Gonna_Give_You_Up_Official_Music_Video_2026-06-07_14-30-22.txt
  8. Reports: 
     ✓ Transcript saved successfully!
     📁 File: output/Rick_Astley_-_Never_Gonna_Give_You_Up_Official_Music_Video_2026-06-07_14-30-22.txt
     📊 Size: 45.2 KB (46,289 bytes)
     📝 Lines: 1,234
     🔤 Words: ~8,910

Base directory for this skill: file:///home/hiennhan/Desktop/claude-test/.claude/skills/youtube-videos-transcript
Relative paths in this skill (e.g., scripts/, reference/) are relative to this base directory.
Note: file list is sampled.