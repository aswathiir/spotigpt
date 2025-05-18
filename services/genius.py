import lyricsgenius
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class LyricsService:
    def __init__(self):
        genius_token = os.getenv("GENIUS_API_TOKEN")
        if not genius_token:
            raise ValueError("Genius API token not found in .env file")
        
        # Rate limit: 5 requests per second
        self.genius = lyricsgenius.Genius(genius_token, 
                                         skip_non_songs=True,
                                         excluded_terms=["(Remix)", "(Live)"],
                                         remove_section_headers=True)
        self.genius.verbose = False
        self.genius.timeout = 15
    
    def get_lyrics(self, artist: str, song: str) -> Optional[str]:
        """Get lyrics for a song (free tier available)"""
        try:
            song = self.genius.search_song(song, artist)
            return song.lyrics if song else None
        except Exception as e:
            print(f"Error getting lyrics: {e}")
            return None