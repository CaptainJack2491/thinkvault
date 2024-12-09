import os
import re
import subprocess

def get_transcript(video_url, output_file="transcript.txt"):
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
        
        # Step 3: Convert .vtt to plain text
        with open(vtt_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Clean up timestamps and formatting
        plain_text = re.sub(r"\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+\n", "", content)  # Remove timestamps
        plain_text = re.sub(r"<[^>]+>", "", plain_text)  # Remove tags
        plain_text = re.sub(r"\n{2,}", "\n", plain_text).strip()  # Remove extra newlines
        
        # Save cleaned transcript to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(plain_text)
        
        print(f"Transcript saved to {output_file}")
        
        # Cleanup: Remove the original .vtt file
        os.remove(vtt_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter the video URL: ")
    get_transcript(video_url)

