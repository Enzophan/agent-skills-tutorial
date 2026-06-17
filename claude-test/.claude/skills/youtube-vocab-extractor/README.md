# YouTube Vocabulary Extractor Skill

This skill extracts potential new words and phrasal verbs from YouTube video transcripts.

## How it Works

1. Extracts the video ID from a YouTube URL
2. Attempts to fetch the English transcript/subtitles using:
   - Primary: `youtube-transcript-api` library
   - Fallback: `yt-dlp` to download auto-generated subtitles
3. Processes the transcript to identify:
   - Less common words (appearing < 3 times, length > 4 characters)
   - Potential phrasal verbs (verb + preposition combinations)

## Limitations

- Works best with videos that have subtitles available (either manually uploaded or auto-generated)
- For videos without subtitles, the skill cannot extract text
- Does NOT extract text from on-screen graphics/highlighted text (would require OCR/video frame analysis)
- Vocabulary identification is heuristic-based (less common words) rather than dictionary-based

## Usage

```bash
# From command line:
python youtube_vocab_extractor.py "<youtube_url>"

# Example:
python youtube_vocab_extractor.py "https://youtu.be/ThbMu47q7Wg?si=Yy2LMZBFzwKNoPNl"
```

## Installation Requirements

The skill requires:
- Python 3.6+
- youtube-transcript-api (installed in virtual environment)
- yt-dlp (installed in virtual environment)

A virtual environment is automatically set up in the skill directory.

## Output Format

The skill outputs results in markdown format:

```
# Vocabulary Extracted from YouTube Video

## New Words
- word1
- word2
- word3

## Phrasal Verbs
- phrasal verb 1
- phrasal verb 2

*Analysis based on X words (Y unique)*
*Note: For highlighted on-screen text, OCR video processing would be required.*
```

## Notes

- For the specific video you referenced (`https://youtu.be/ThbMu47q7Wg?si=Yy2LMZBFzwKNoPNl`), no English subtitles appear to be available, which is why the transcript extraction fails.
- To extract vocabulary from on-screen highlighted text (as mentioned in your request), you would need:
  1. Video download
  2. Frame-by-frame processing
  3. Optical Character Recognition (OCR)
  4. Text styling/position analysis to identify highlighted areas
  This would require significantly more complex computer vision tools.