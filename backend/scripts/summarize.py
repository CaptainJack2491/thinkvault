import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()


def summarize(transcript,thoughts):

    prompt = f"""
    You are an assistant tasked with summarizing a video transcript. Extract the key points, topics, insights, and actionable takeaways. 

    Here is the transcript:
    \"\"\"
    {transcript}
    \"\"\"

    Provide the response in the following format:

    ---
    tags:
        - [Tag 1]
        - [Tag 2]
    ---
    # [Video Title or Description]

    ## Key Points
    - [Bullet point summaries of main ideas]

    ## Detailed Topics
    ### Topic 1: [Topic Title]
    [2-3 sentence explanation or breakdown]

    ## Interesting Insights
    - [Unique, surprising, or noteworthy insights]

    ## Actionable Takeaways
    1. [Takeaway 1]
    2. [Takeaway 2]
    3. [Takeaway 3]

  ## Your Thoughts
    {thoughts}

  ## Your Thoughts (Expanded)
    [AI-generated expansion and insights based on user's thoughts.]


    """




    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "Summarize the content in a markdown format. Keep in mind that this summary will be used to learn and ask more questions so keep it clear and factual. Extract as much knowledge as you can from this transcript"},
        {"role": "user", "content": prompt}
      ]
    )

    return completion.choices[0].message.content

