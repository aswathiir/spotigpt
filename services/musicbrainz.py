import musicbrainzngs
from typing import Dict, List, Optional

class MusicBrainzService:
    def __init__(self):
        musicbrainzngs.set_useragent(
            "SpotiGPT-Music-Chatbot",
            "0.1",
            contact="your@email.com"  # Replace with your email
        )
    
    def get_artist_details(self, artist_name: str) -> Optional[Dict]:
        """Get artist details from MusicBrainz (free)"""
        try:
            result = musicbrainzngs.search_artists(artist=artist_name, limit=1)
            if result['artist-list']:
                artist_id = result['artist-list'][0]['id']
                return musicbrainzngs.get_artist_by_id(artist_id, includes=["url-rels"])
            return None
        except Exception as e:
            print(f"Error getting artist details: {e}")
            return None
    
    def get_album_info(self, album_name: str, artist_name: str) -> Optional[Dict]:
        """Get album information"""
        try:
            result = musicbrainzngs.search_releases(
                release=album_name,
                artist=artist_name,
                limit=1
            )
            if result['release-list']:
                release_id = result['release-list'][0]['id']
                return musicbrainzngs.get_release_by_id(release_id, includes=["recordings"])
            return None
        except Exception as e:
            print(f"Error getting album info: {e}")
            return None