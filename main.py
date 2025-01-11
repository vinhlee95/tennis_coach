import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  system_instruction="""
  You are a helpful assistant that can format the input into a YouTube search query.
  The query should be used to find a video tutorial to improve the technique for the player.
  For example: "how to improve backhand for beginner tennis player",
  """
)

# Get input for YouTube search video
keywords = [
  "Intermediate",
  "Forehand",
  "Eastern grip",
]

response = model.generate_content(
  f"""
  Use following keywords to generate a YouTube search query:
  {", ".join(keywords)}
  """
)

print(response.text)