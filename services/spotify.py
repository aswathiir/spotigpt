import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

load_dotenv()

class SpotifyService:
    def __init__(self):
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not found in .env file")
        
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
    
    def search_track(self, query: str) -> Optional[Dict]:
        """Search for a track (free tier allows 30 requests per minute)"""
        results = self.sp.search(q=query, limit=1, type='track')
        if results['tracks']['items']:
            return results['tracks']['items'][0]
        return None
    
    def get_recommendations(self, seed_tracks: List[str], limit: int = 5) -> List[Dict]:
        """Get track recommendations (free tier available)"""
        try:
            results = self.sp.recommendations(seed_tracks=seed_tracks, limit=limit)
            return results['tracks']
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_artist_info(self, artist_id: str) -> Optional[Dict]:
        """Get artist information"""
        try:
            return self.sp.artist(artist_id)
        except Exception as e:
            print(f"Error getting artist info: {e}")
            return None
    
    def get_track_features(self, track_id: str) -> Optional[Dict]:
        """Get audio features for a track"""
        try:
            return self.sp.audio_features([track_id])[0]
        except Exception as e:
            print(f"Error getting track features: {e}")
            return None