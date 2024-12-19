import os
import re
import subprocess
from urllib.parse import urlparse, parse_qs

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root directory
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")  # Path to transcripts folder

# Ensure the transcripts folder exists
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

def extract_video_id(url):
    """Extracts the YouTube video ID from a URL."""
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")
    return None

def get_transcript(video_url):
    try:
        # Extract video ID for filenames
        video_id = extract_video_id(video_url)
        if not video_id:
            print("Error: Could not extract video ID.")
            return

        # Define filenames based on video ID
        raw_filename = f"{video_id}_raw.txt"
        clean_filename = f"{video_id}_clean.txt"
        raw_output = os.path.join(TRANSCRIPTS_DIR, raw_filename)
        clean_output = os.path.join(TRANSCRIPTS_DIR, clean_filename)

        # Step 1: Download the subtitles using yt-dlp
        print("Fetching subtitles...")
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub", "--sub-lang", "en", "--skip-download",
            "-o", "transcript.%(ext)s", video_url
        ], check=True)

        # Step 2: Find the downloaded .vtt file
        vtt_file = next(f for f in os.listdir() if f.endswith(".vtt"))

        # Define full paths for raw and clean transcripts
        raw_output = os.path.join(TRANSCRIPTS_DIR, raw_output)
        clean_output = os.path.join(TRANSCRIPTS_DIR, clean_output)

        # Step 3: Process the raw transcript
        print(f"Saving raw transcript to {raw_output}...")
        with open(vtt_file, "r", encoding="utf-8") as f:
            raw_content = f.read()

        with open(raw_output, "w", encoding="utf-8") as f:
            f.write(raw_content)

        # Step 4: Clean and deduplicate the transcript
        print(f"Cleaning transcript and saving to {clean_output}...")
        lines = raw_content.splitlines()
        cleaned_lines = []
        seen_lines = set()

        for line in lines:
            # Remove metadata lines (WEBVTT, Kind:, Language:)
            if re.match(r"^(WEBVTT|Kind:|Language:)", line):
                continue

            # Remove timing lines and alignment tags
            if re.match(r"\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+", line):
                continue
            if "align:" in line or "position:" in line:
                continue

            # Remove timestamps, tags, sequence numbers, and extra newlines
            plain_text = re.sub(r"\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+\n", "", line)  # Remove timestamps
            plain_text = re.sub(r"<[^>]+>", "", plain_text)  # Remove tags
            plain_text = re.sub(r"^\d+\n", "", plain_text, flags=re.MULTILINE)  # Remove sequence numbers
            plain_text = re.sub(r"\n{2,}", "\n", plain_text).strip()  # Remove extra newlines
            clean_line = plain_text.strip()

            # Remove empty lines and deduplicate
            if clean_line and clean_line not in seen_lines:
                cleaned_lines.append(clean_line)
                seen_lines.add(clean_line)

        # Write cleaned transcript
        with open(clean_output, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines))

        print(f"Transcripts saved: {raw_output} (raw), {clean_output} (clean)")

        # Step 5: Cleanup the original .vtt file
        os.remove(vtt_file)
        print("Temporary files cleaned up.")

        return raw_output, clean_output

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter the video URL: ")
    get_transcript(video_url)

