import os
import re
import subprocess

def get_transcript(video_url, raw_output="transcript_raw.txt", clean_output="transcript_clean.txt"):
    try:
        # Step 1: Download the subtitles using yt-dlp
        print("Fetching subtitles...")
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub", "--sub-lang", "en", "--skip-download",
            "-o", "transcript.%(ext)s", video_url
        ], check=True)

        # Step 2: Find the downloaded .vtt file
        vtt_file = next(f for f in os.listdir() if f.endswith(".vtt"))

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

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter the video URL: ")
    get_transcript(video_url)

