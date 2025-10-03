from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_lecture(transcript):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {"role": "system", "content": "You are an expert summarization assistant who can create clear, concise, and structured notes from any transcript."},
            {"role": "user", "content": f"""Here is a transcript:
{transcript}

Your task:
- Summarize the transcript into easy-to-read notes.
- Organize the content under clear headings and subheadings.
- Highlight important points, concepts, and examples where applicable.
- Use '-' for bullet points (avoid using '*' or '+').
- Use '**' for bold only for key terms, not every bullet.
- Keep it concise, clean, and visually appealing.
- Suitable for someone wanting a quick but complete understanding.

Generate the summary notes accordingly."""}
        ]
    )

    return response.choices[0].message.content
def chat_with_transcript(transcript, history):
    """Chatbot that answers based on transcript + conversation history"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant. Use only the transcript to answer. Maintain conversation flow."},
            {"role": "system", "content": f"Transcript:\n{transcript}"}
        ] + history
    )

    return response.choices[0].message.content

