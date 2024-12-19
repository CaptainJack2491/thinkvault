from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.get_data import get_transcript
from scripts.summarize import summarize
from scripts.markdown import save_markdown

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/process', methods=['POST'])
def process_data():
    data = request.json
    link = data.get('link')
    thoughts = data.get('thoughts')

    # Process the data
    result = {
        "message": f"Received link: {link} and thoughts: {thoughts}"
    }
    raw_transcript,clean_transcript = get_transcript(link)
    print("Transcript saved successfully!")
    with open(clean_transcript, "r", encoding="utf-8") as f:
        summary = f.read()

    summary_content = summarize(summary,thoughts)
    save_markdown(link, summary_content)
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000)
