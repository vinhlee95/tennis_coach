import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from youtube_client import YouTubeAPI

app = Flask(__name__)

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

@app.route('/api/tutorials')
def get_tutorials():
    # Get keywords from query parameters, defaulting to empty list if not provided
    keywords_param = request.args.get('keywords', '')
    keywords = [k.strip() for k in keywords_param.split(',')] if keywords_param else []

    # Fallback to default keywords if none provided
    if not keywords:
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

    # Transform videos data to include additional details
    enriched_videos = []
    for video in videos:
        video_data = {
            'title': video['title'],
            'channel': video['channel'],
            'url': video['url'],
        }
        
        # Get additional details
        details = youtube.get_video_details(video['video_id'])
        if details:
            video_data.update({
                'views': details.get('view_count', 'N/A'),
                'likes': details.get('like_count', 'N/A')
            })
        
        enriched_videos.append(video_data)

    return jsonify({
        'videos': enriched_videos
    })

if __name__ == '__main__':
    app.run(debug=True)

