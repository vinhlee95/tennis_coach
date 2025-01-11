import os
import google.generativeai as genai
from dotenv import load_dotenv

from youtube_client import YouTubeAPI

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
query = response.text

youtube = YouTubeAPI(os.getenv("YOUTUBE_API_KEY") or "")
videos = youtube.search_videos(
  query=query,
  max_results=5,
  language="en",
  region_code="US",
  relevance_language="en",
)

# Print results
for video in videos:
    print(f"\nTitle: {video['title']}")
    print(f"Channel: {video['channel']}")
    print(f"URL: {video['url']}")
    
    # Get additional details
    details = youtube.get_video_details(video['video_id'])
    if details:
        print(f"Views: {details.get('view_count', 'N/A')}")
        print(f"Likes: {details.get('like_count', 'N/A')}")

