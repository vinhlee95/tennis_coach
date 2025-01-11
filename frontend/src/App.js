import { useState } from 'react';
import axios from 'axios';
import {
  Container,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  CircularProgress,
  IconButton,
} from '@mui/material';
import { Search, ThumbUp, Visibility } from '@mui/icons-material';

function App() {
  const [keywords, setKeywords] = useState('');
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.get(`/api/tutorials?keywords=${encodeURIComponent(keywords)}`);
      setVideos(response.data.videos);
    } catch (error) {
      console.error('Error fetching tutorials:', error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        Tennis Tutorial Finder
      </Typography>

      <Box component="form" onSubmit={handleSearch} sx={{ mb: 4, textAlign: 'center' }}>
        <TextField
          fullWidth
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="Enter keywords (comma-separated)"
          variant="outlined"
          sx={{ maxWidth: 600, mb: 2 }}
        />
        <Button
          type="submit"
          variant="contained"
          size="large"
          startIcon={<Search />}
          disabled={loading}
        >
          Search
        </Button>
      </Box>

      {loading && (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      )}

      <Grid container spacing={3}>
        {videos.map((video, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="180"
                image={video.thumbnail || `https://i.ytimg.com/vi/${getVideoId(video.url)}/mqdefault.jpg`}
                alt={video.title}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="h2" sx={{
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                }}>
                  {video.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {video.channel}
                </Typography>
                <Box display="flex" alignItems="center" gap={2}>
                  <Box display="flex" alignItems="center">
                    <Visibility sx={{ fontSize: 18, mr: 0.5 }} />
                    <Typography variant="body2" color="text.secondary">
                      {formatNumber(video.views)}
                    </Typography>
                  </Box>
                  <Box display="flex" alignItems="center">
                    <ThumbUp sx={{ fontSize: 18, mr: 0.5 }} />
                    <Typography variant="body2" color="text.secondary">
                      {formatNumber(video.likes)}
                    </Typography>
                  </Box>
                </Box>
                <Button
                  variant="outlined"
                  href={video.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{ mt: 2 }}
                  fullWidth
                >
                  Watch Video
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

// Helper function to format numbers (e.g., 1000 -> 1K)
function formatNumber(num) {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}

// Helper function to extract video ID from YouTube URL
function getVideoId(url) {
  const match = url.match(/(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/user\/\S+|\/ytscreeningroom\?v=|\/sandalsResorts#\w\/\w\/.*\/))([^\/&\?]{10,12})/);
  return match ? match[1] : '';
}

export default App; 