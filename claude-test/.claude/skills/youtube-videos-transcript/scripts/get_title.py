#!/usr/bin/env python3
"""
Fetch the title of a YouTube video using yt-dlp.
Usage: python get_title.py <video_url>
Output: Sanitized title string safe for filenames, or an error message.
"""
import sys
import re
import subprocess
import json

def sanitize_filename(title: str) -> str:
    """
    Sanitize a string to be safe for use in filenames.
    Removes or replaces special characters that are invalid in file paths.
    """
    title = title.strip()
    # Replace path separators and other invalid characters
    title = re.sub(r'[\\/:*?"<>|]', '_', title)
    # Remove any control characters or newlines
    title = re.sub(r'[\x00-\x1f\x7f]', '', title)
    # Replace multiple consecutive underscores with a single one
    title = re.sub(r'_+', '_', title)
    # Remove leading/trailing underscores and dots
    title = title.strip('_.')
    # Ensure the filename is not empty
    if not title:
        title = "youtube_video"
    return title

def fetch_title(video_url: str):
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", video_url],
            capture_output=True,
            text=True,
            check=True,
        )
        title = result.stdout.strip()
        return sanitize_filename(title)
    except FileNotFoundError:
        return {"error": "yt-dlp not found. Please install it: pip install yt-dlp"}
    except subprocess.CalledProcessError as e:
        return {"error": f"yt-dlp failed: {e.stderr.strip()}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_title.py <video_url>", file=sys.stderr)
        sys.exit(1)

    video_url = sys.argv[1]
    result = fetch_title(video_url)
    if isinstance(result, dict) and "error" in result:
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    else:
        print(result)