from scripts.get_data import get_transcript
from scripts.summarize import summarize
from scripts.markdown import save_markdown

def main():
    link = input("Enter the video/article link: ")
    thoughts = input("Enter your thoughts: ")
    raw_transcript,clean_transcript = get_transcript(link)
    print("Transcript saved successfully!")
    with open(clean_transcript, "r", encoding="utf-8") as f:
        summary = f.read()

    summary_content = summarize(summary,thoughts)
    save_markdown(link, summary_content)



if __name__ == "__main__":
    main()

