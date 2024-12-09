from scripts.get_data import get_transcript
from scripts.summarize import summarize

def main():
    link = input("Enter the video/article link: ")
    raw_transcript,clean_transcript = get_transcript(link)
    print("Transcript saved successfully!")
    with open(clean_transcript, "r", encoding="utf-8") as f:
        summary = summarize(f.read())

    print(summary)



if __name__ == "__main__":
    main()

