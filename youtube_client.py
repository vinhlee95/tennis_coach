from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict
import logging

class YouTubeAPI:
  def __init__(self, api_key: str):
      self.youtube = build('youtube', 'v3', developerKey=api_key)
      self.logger = logging.getLogger(__name__)

  def search_videos(
      self, 
      query: str, 
      max_results: int = 5,
      language: str = 'en',
      region_code: str = 'US',
      relevance_language: str = 'en',
      order: str = 'relevance',
  ) -> List[Dict]:
      """
      Search YouTube videos based on query
      """
      print(f"🔎 Searching for videos with query: {query}")
      
      try:
          request = self.youtube.search().list(
              part="snippet",
              q=query,
              type="video",          # Only return videos (not playlists/channels)
              maxResults=max_results,
              order=order,
              videoEmbeddable="true", # Only videos that can be embedded
              relevanceLanguage=relevance_language,
              regionCode=region_code,
              fields="items(id(videoId),snippet(title,description,publishedAt,channelTitle,thumbnails))"
          )

          response = request.execute()

          videos = []
          for item in response['items']:
              video = {
                  'video_id': item['id']['videoId'],
                  'title': item['snippet']['title'],
                  'description': item['snippet']['description'],
                  'channel': item['snippet']['channelTitle'],
                  'published_at': item['snippet']['publishedAt'],
                  'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                  'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
              }
              videos.append(video)

          return videos

      except HttpError as e:
          self.logger.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
          return []
      except Exception as e:
          self.logger.error(f"An error occurred: {str(e)}")
          return []

  def get_video_details(self, video_id: str) -> Dict:
      """
      Get additional details for a specific video
      """
      try:
          request = self.youtube.videos().list(
              part="statistics,contentDetails",
              id=video_id
          )
          response = request.execute()

          if response['items']:
              stats = response['items'][0]
              return {
                  'view_count': stats['statistics'].get('viewCount'),
                  'like_count': stats['statistics'].get('likeCount'),
                  'comment_count': stats['statistics'].get('commentCount'),
                  'duration': stats['contentDetails']['duration']
              }
          return {}

      except Exception as e:
          self.logger.error(f"Error getting video details: {str(e)}")
          return {}