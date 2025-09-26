from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
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
- Highlight important points, decisions, concepts, and examples where applicable.
- Use bullet points for clarity.
- Keep it concise and ensure the key information is easy to understand.
- Make it suitable for someone who wants a quick but complete understanding of the transcript.

Generate the summary notes accordingly."""}
        ]
    )


    # Correct way to access the content from the response
    return response.choices[0].message.content


# from groq import Groq
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Initialize Groq client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def analyze_lecture(transcript):
#     response = client.chat.completions.create(
#         model="meta-llama/llama-4-maverick-17b-128e-instruct",  # Replace with your desired model
#         messages=[
#             {"role": "system", "content": "You are an expert meeting assistant."},
#             {"role": "user", "content": f"""Here is a meeting transcript:
# {transcript}

# Summarize the key points, list the action items, decisions made, and generate a follow-up email."""}
#         ]
#     )
    
#     return response.choices[0].message["content"]

# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Initialize the Groq model
# llm = ChatGroq(
#     model_name="meta-llama/llama-4-maverick-17b-128e-instruct",  # Free, fast Groq-hosted model
#     temperature=0.0,
#     groq_api_key=os.getenv("GROQ_API_KEY"),  # Ensure your API key is set in .env
# )

# def analyze_lecture(transcript):
#     # Send transcript to the model
#     response = llm.chat(
#         [
#             {"role": "system", "content": "You are an expert meeting assistant."},
#             {
#                 "role": "user",
#                 "content": f"""Here is a meeting transcript:
# {transcript}

# Summarize the key points, list the action items, decisions made, and generate a follow-up email."""
#             }
#         ]
#     )
    
#     return response.message["content"]
