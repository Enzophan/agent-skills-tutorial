#!/usr/bin/env python3
"""
Fetch the English transcript from a YouTube video using youtube-transcript-api.
Usage: python get_transcript.py <video_id>
Output: JSON list with 'text' and optional 'start' fields, or an error message.
"""
import sys
import json
import time

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Error: youtube-transcript-api is not installed. Run 'pip install youtube-transcript-api'", file=sys.stderr)
    sys.exit(1)

def fetch_transcript(video_id: str, max_retries: int = 2):
    """
    Fetch transcript with retry mechanism for network errors.
    """
    for attempt in range(max_retries + 1):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            return transcript
        except Exception as e:
            error_str = str(e).lower()
            # If it's a network-related error and we have retries left, wait and retry
            if attempt < max_retries and ('connection' in error_str or 'timeout' in error_str or 'network' in error_str):
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            # Otherwise, return the error
            return {"error": str(e)}
    
    # This shouldn't be reached, but just in case
    return {"error": "Failed to retrieve transcript after multiple attempts"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_transcript.py <video_id>", file=sys.stderr)
        sys.exit(1)

    video_id = sys.argv[1]
    result = fetch_transcript(video_id)
    print(json.dumps(result, ensure_ascii=False))