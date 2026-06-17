#!/usr/bin/env python3
"""
YouTube Vocabulary Extractor Skill - Enhanced Version
Downloads YouTube videos, extracts audio, transcribes to text, and saves transcript
Also extracts vocabulary from transcripts when available
"""

import re
import sys
import json
import os
import subprocess
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    # Handle youtu.be format
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]

    # Handle youtube.com format
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]

    return None

def download_youtube_video(video_id, output_dir="/tmp"):
    """Download YouTube video using yt-dlp"""
    try:
        # Download video in best available format
        output_template = os.path.join(output_dir, f"{video_id}.%(ext)s")
        result = subprocess.run([
            'yt-dlp',
            '-f', 'best[ext=mp4]/best',
            '-o', output_template,
            f'https://www.youtube.com/watch?v={video_id}'
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            # Find the downloaded file
            import glob
            video_files = glob.glob(os.path.join(output_dir, f"{video_id}.*"))
            if video_files:
                return video_files[0]
        else:
            print(f"WARNING: yt-dlp failed: {result.stderr}")
            
    except Exception as e:
        print(f"WARNING: Error downloading video: {e}")
    
    return None

def extract_audio_to_mp3(video_file, output_dir="/tmp"):
    """Extract audio from video file and convert to MP3"""
    try:
        audio_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(video_file))[0]}.mp3")
        
        # Use ffmpeg to extract audio
        result = subprocess.run([
            'ffmpeg',
            '-i', video_file,
            '-vn',  # No video
            '-acodec', 'libmp3lame',  # MP3 codec
            '-q:a', '2',  # High quality
            audio_file
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(audio_file):
            return audio_file
        else:
            print(f"WARNING: ffmpeg failed: {result.stderr}")
            
    except Exception as e:
        print(f"WARNING: Error extracting audio: {e}")
    
    return None

def transcribe_audio_to_text(audio_file):
    """Transcribe audio file to text using speech recognition"""
    try:
        import speech_recognition as sr
        from pydub import AudioSegment
        
        # Convert MP3 to WAV for speech recognition (required by some recognizers)
        wav_file = os.path.splitext(audio_file)[0] + ".wav"
        
        # Convert audio to WAV
        audio = AudioSegment.from_mp3(audio_file)
        audio.export(wav_file, format="wav")
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Process audio file
        with sr.AudioFile(wav_file) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Record the audio
            audio_data = recognizer.record(source)
        
        # Try Google Speech Recognition first (free tier)
        try:
            text = recognizer.recognize_google(audio_data)
            print("INFO: Used Google Speech Recognition")
            return text
        except sr.RequestError:
            # Fallback to offline recognition if available
            try:
                text = recognizer.recognize_sphinx(audio_data)
                print("INFO: Used CMU Sphinx (offline) recognition")
                return text
            except:
                print("WARNING: Speech recognition failed")
                return None
        except sr.UnknownValueError:
            print("WARNING: Could not understand audio")
            return None
            
    except ImportError as e:
        print(f"WARNING: Missing speech recognition dependencies: {e}")
        return None
    except Exception as e:
        print(f"WARNING: Error transcribing audio: {e}")
        return None
    finally:
        # Clean up temporary WAV file
        if 'wav_file' in locals() and os.path.exists(wav_file):
            try:
                os.remove(wav_file)
            except:
                pass

def save_transcript(text, video_id, output_dir="./.claude/skills/youtube-vocab-extractor/output"):
    """Save transcript to text file"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        transcript_file = os.path.join(output_dir, f"transcript_{video_id}.txt")
        
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return transcript_file
    except Exception as e:
        print(f"WARNING: Error saving transcript: {e}")
        return None

def get_transcript_from_subtitles(video_id):
    """Fetch transcript using youtube-transcript-api or fallback method"""
    try:
        # Try to use youtube-transcript-api if available
        result = subprocess.run([
            sys.executable, '-c',
            f'''
import sys
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    transcript_list = YouTubeTranscriptApi.get_transcript("{video_id}", languages=['en'])
    transcript_text = " ".join([item['text'] for item in transcript_list])
    print(transcript_text)
except Exception as e:
    print(f"ERROR: {{e}}", file=sys.stderr)
    sys.exit(1)
'''
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0 and not result.stdout.startswith("ERROR:"):
            return result.stdout.strip()
        else:
            # Fallback: try to get auto-generated captions via youtube-dl/yt-dlp
            return get_transcript_fallback(video_id)

    except Exception as e:
        return get_transcript_fallback(video_id)

def get_transcript_fallback(video_id):
    """Fallback method to get transcript using yt-dlp or similar"""
    try:
        # Try yt-dlp to get subtitles
        result = subprocess.run([
            'yt-dlp',
            '--skip-download',
            '--write-auto-sub',
            '--sub-lang', 'en',
            '--sub-format', 'srt',
            '-o', '/tmp/%(id)s.%(ext)s',
            f'https://www.youtube.com/watch?v={video_id}'
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            # Read the generated SRT file
            import glob
            srt_files = glob.glob(f'/tmp/{video_id}.*.srt')
            if srt_files:
                with open(srt_files[0], 'r', encoding='utf-8') as f:
                    srt_content = f.read()
                # Convert SRT to plain text
                return srt_to_plain_text(srt_content)
    except Exception:
        pass

    return None

def srt_to_plain_text(srt_content):
    """Convert SRT subtitle format to plain text"""
    # Remove SRT timing and formatting
    lines = srt_content.split('\n')
    text_lines = []

    for line in lines:
        line = line.strip()
        # Skip line numbers and timing lines
        if not line or line.isdigit() or '-->' in line:
            continue
        # Remove HTML tags if present
        line = re.sub(r'<[^>]+>', '', line)
        text_lines.append(line)

    return ' '.join(text_lines)

def extract_vocabulary(text):
    """Extract potential new words and phrasal verbs from text"""
    # Clean the text
    text = re.sub(r'[^\w\s\-]', ' ', text)  # Keep words, spaces, and hyphens
    text = re.sub(r'\s+', ' ', text).strip().lower()

    words = text.split()

    # Common words to filter out (basic stop words)
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his',
        'hers', 'ours', 'theirs', 'what', 'which', 'who', 'whom', 'whose', 'where',
        'when', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
        'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 's', 't', 'don', 'now', 'd', 'll', 'm', 'o', 're',
        've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven',
        'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren',
        'won', 'wouldn'
    }

    # Filter out stop words and very short words
    content_words = [w for w in words if w not in stop_words and len(w) > 2]

    # Count word frequency
    from collections import Counter
    word_freq = Counter(content_words)

    # Get less common words (appearing less than 3 times) as potential vocabulary
    less_common = [(word, freq) for word, freq in word_freq.items() if freq < 3 and len(word) > 4]
    less_common.sort(key=lambda x: x[1])  # Sort by frequency (rarest first)

    # Extract potential phrasal verbs (verb + preposition combinations)
    phrasal_verbs = extract_phrasal_verbs(text)

    return {
        'new_words': [word for word, freq in less_common[:20]],  # Top 20 rarer words
        'phrasal_verbs': phrasal_verbs[:10],  # Top 10 phrasal verbs
        'total_words_analyzed': len(words),
        'unique_words': len(word_freq)
    }

def extract_phrasal_verbs(text):
    """Extract potential phrasal verbs from text"""
    # Common phrasal verb patterns
    common_verbs = [
        'get', 'go', 'come', 'run', 'take', 'make', 'put', 'give', 'turn',
        'look', 'bring', 'pick', 'hold', 'break', 'carry', 'catch', 'fall',
        'hold', 'keep', 'let', 'put', 'run', 'set', 'sit', 'stand', 'take',
        'turn', 'work', 'write'
    ]

    common_prepositions = [
        'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'away', 'back', 'by', 'for', 'from', 'into', 'through', 'together',
        'towards', 'upon', 'with', 'without'
    ]

    words = text.split()
    phrasal_verbs_found = []

    for i in range(len(words) - 1):
        verb = words[i]
        prep = words[i + 1]

        if verb in common_verbs and prep in common_prepositions:
            phrasal_verbs_found.append(f"{verb} {prep}")

    # Remove duplicates while preserving order
    seen = set()
    unique_phrasal = []
    for pv in phrasal_verbs_found:
        if pv not in seen:
            seen.add(pv)
            unique_phrasal.append(pv)

    return unique_phrasal

def main():
    if len(sys.argv) != 2:
        print("Usage: youtube_vocab_extractor.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)

    if not video_id:
        print("ERROR: Could not extract video ID from URL")
        sys.exit(1)

    print(f"INFO: Processing video ID: {video_id}")

    # First, try to get transcript from subtitles (faster)
    transcript = get_transcript_from_subtitles(video_id)
    
    if transcript:
        print("INFO: Retrieved transcript from subtitles")
    else:
        print("INFO: No subtitles available, downloading video and extracting audio...")
        
        # Download video
        video_file = download_youtube_video(video_id)
        if not video_file:
            print("ERROR: Could not download YouTube video")
            sys.exit(1)
        
        print(f"INFO: Downloaded video to: {video_file}")
        
        # Extract audio to MP3
        audio_file = extract_audio_to_mp3(video_file)
        if not audio_file:
            print("ERROR: Could not extract audio from video")
            # Clean up video file
            try:
                os.remove(video_file)
            except:
                pass
            sys.exit(1)
        
        print(f"INFO: Extracted audio to: {audio_file}")
        
        # Transcribe audio to text
        transcript = transcribe_audio_to_text(audio_file)
        if not transcript:
            print("ERROR: Could not transcribe audio to text")
            # Clean up files
            try:
                os.remove(video_file)
                os.remove(audio_file)
            except:
                pass
            sys.exit(1)
        
        print(f"INFO: Transcribed audio to text ({len(transcript)} characters)")
        
        # Save transcript to output folder
        transcript_file = save_transcript(transcript, video_id)
        if transcript_file:
            print(f"INFO: Saved transcript to: {transcript_file}")
        else:
            print("WARNING: Could not save transcript file")
        
        # Clean up temporary files
        try:
            os.remove(video_file)
            os.remove(audio_file)
        except:
            pass

    # Extract vocabulary from transcript (if we have one)
    if transcript:
        print("INFO: Extracting vocabulary from transcript...")
        vocab_data = extract_vocabulary(transcript)
        
        # Output as markdown (maintaining backward compatibility)
        print("# Vocabulary Extracted from YouTube Video")
        print()
        print("## New Words")
        if vocab_data['new_words']:
            for word in vocab_data['new_words']:
                print(f"- {word}")
        else:
            print("- No distinctive vocabulary found")
        print()
        print("## Phrasal Verbs")
        if vocab_data['phrasal_verbs']:
            for pv in vocab_data['phrasal_verbs']:
                print(f"- {pv}")
        else:
            print("- No phrasal verbs detected")
        print()
        print(f"*Analysis based on {vocab_data['total_words_analyzed']} words ({vocab_data['unique_words']} unique)*")
        print("*Note: Transcript obtained via audio processing when subtitles unavailable.*")
    else:
        print("ERROR: No transcript available for vocabulary extraction")

if __name__ == "__main__":
    main()
