import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()


def summarize(transcript):
    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": "Summarize the content in a markdown format. Keep in mind that this summary will be used to learn and ask more questions so keep it clear and factual"},
        {"role": "user", "content": transcript}
      ]
    )

    return completion.choices[0].message.content

