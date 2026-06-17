#!/usr/bin/env python3
"""
Validate YouTube URLs.
Usage: python validate_url.py <url>
Output: JSON with validation result and extracted video ID if valid.
"""
import sys
import json
import re
from urllib.parse import urlparse, parse_qs

def validate_youtube_url(url: str):
    """
    Validate a YouTube URL and extract the video ID.
    Returns a dictionary with validation results.
    """
    if not url or not isinstance(url, str):
        return {"valid": False, "error": "URL must be a non-empty string"}
    
    url = url.strip()
    
    # Patterns for YouTube URLs
    patterns = [
        # Standard YouTube URL: https://www.youtube.com/watch?v=VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\\n\\s]+)',
        # Shortened YouTube URL: https://youtu.be/VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtu\.be/([^\\n\\s]+)',
        # Embedded YouTube URL: https://www.youtube.com/embed/VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^\\n\\s]+)',
    ]
    
    video_id = None
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            video_id = match.group(1)
            # Basic validation: YouTube video IDs are typically 11 characters
            # but can vary, so we'll accept any non-empty string for now
            if video_id:
                break
    
    if video_id:
        return {
            "valid": True,
            "video_id": video_id,
            "url": url
        }
    else:
        return {
            "valid": False,
            "error": "Invalid YouTube URL. Supported formats:\n"
                   "- https://www.youtube.com/watch?v=VIDEO_ID\n"
                   "- https://youtu.be/VIDEO_ID\n"
                   "- https://www.youtube.com/embed/VIDEO_ID"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_url.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    result = validate_youtube_url(url)
    print(json.dumps(result, ensure_ascii=False))
    
    # Exit with error code if invalid
    if not result.get("valid", False):
        sys.exit(1)