import os
import scripts.get_data as get_data

def save_markdown(video_url, summary_content):
    """
    Saves the AI-generated summary content to a Markdown file.
    """
    video_id = get_data.extract_video_id(video_url)
    filename = f"{video_id}_summary.md"

    output_dir = "summaries"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    print(f"Saving summary to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(summary_content)

    print(f"Summary saved successfully as {filename}!")


