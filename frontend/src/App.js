import { useState } from 'react';
import axios from 'axios';

function App() {
  const [keywords, setKeywords] = useState('');
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.get(`/api/tutorials?keywords=${encodeURIComponent(keywords)}`);
      console.log(response.data.videos);
      setVideos(response.data.videos);
    } catch (error) {
      console.error('Error fetching tutorials:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>Tennis Tutorial Finder</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="Enter keywords (comma-separated)"
          style={{ width: '300px', padding: '8px' }}
        />
        <button type="submit" style={{ marginLeft: '10px' }}>
          Search
        </button>
      </form>

      {loading && <p>Loading...</p>}
      
      <div style={{ marginTop: '20px' }}>
        {videos.map((video, index) => (
          <div key={index} style={{ marginBottom: '20px', border: '1px solid #ccc', padding: '10px' }}>
            <h3>{video.title}</h3>
            <p>Channel: {video.channel}</p>
            <p>Views: {video.views}</p>
            <p>Likes: {video.likes}</p>
            <a href={video.url} target="_blank" rel="noopener noreferrer">
              Watch Video
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App; 