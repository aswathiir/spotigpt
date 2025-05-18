import os
from dotenv import load_dotenv
import cohere
from utils.database import VectorDB
from utils.embeddings import Embedder
from services.spotify import SpotifyService
from services.genius import LyricsService
from services.musicbrainz import MusicBrainzService

load_dotenv()

class EnhancedMusicChatbot:
    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))
        self.db = VectorDB()
        self.embedder = Embedder()
        self.spotify = SpotifyService()
        self.lyrics = LyricsService()
        self.musicbrainz = MusicBrainzService()
        self.setup_knowledge_base()
    
    def setup_knowledge_base(self):
        # Load from text files
        documents = []
        metadatas = []
        
        # Load music theory
        with open("data/music_theory.txt", "r") as f:
            theory = f.read().split("\n\n")
            documents.extend(theory)
            metadatas.extend([{"source": "music_theory", "type": "theory"}] * len(theory))
        
        # Load FAQs
        with open("data/spotify_faqs.txt", "r") as f:
            faqs = f.read().split("\n\n")
            documents.extend(faqs)
            metadatas.extend([{"source": "spotify_faq", "type": "how_to"}] * len(faqs))
        
        # Add to vector DB
        ids = [f"doc_{i}" for i in range(len(documents))]
        self.db.add_documents(documents, metadatas, ids)
    
    def generate_response(self, query: str) -> str:
        # Check if it's a music discovery query
        if any(keyword in query.lower() for keyword in ["play", "song", "track", "artist", "album"]):
            return self.handle_music_query(query)
        
        # Default to RAG for general knowledge
        results = self.db.query(query)
        context = "\n\n".join(results['documents'][0])
        
        prompt = f"""
        You are SpotiGPT, an advanced music assistant. Use the context below to answer.
        Be knowledgeable about music theory, history, and technology.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:"""
        
        response = self.co.generate(
            model="command",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
            stop_sequences=["\n\n"]
        )
        
        return response.generations[0].text
    
    def handle_music_query(self, query: str) -> str:
        """Handle music-specific queries using APIs"""
        try:
            # Try to find a track
            track = self.spotify.search_track(query)
            if track:
                response = f"I found this track: {track['name']} by {track['artists'][0]['name']}\n"
                response += f"Album: {track['album']['name']}\n"
                response += f"Spotify URL: {track['external_urls']['spotify']}\n\n"
                
                # Get recommendations
                recs = self.spotify.get_recommendations([track['id']])
                if recs:
                    response += "You might also like:\n"
                    for i, rec in enumerate(recs[:3], 1):
                        response += f"{i}. {rec['name']} by {rec['artists'][0]['name']}\n"
                
                # Get lyrics if asked
                if "lyric" in query.lower() or "word" in query.lower():
                    lyrics = self.lyrics.get_lyrics(
                        track['artists'][0]['name'],
                        track['name']
                    )
                    if lyrics:
                        response += f"\nHere are some lyrics:\n{lyrics[:300]}..."  # Truncate
                
                return response
            
            # Try artist info
            artist_info = self.musicbrainz.get_artist_details(query)
            if artist_info:
                response = f"Artist: {artist_info['name']}\n"
                if 'type' in artist_info:
                    response += f"Type: {artist_info['type']}\n"
                if 'life-span' in artist_info:
                    response += f"Active: {artist_info['life-span']['begin']} to {artist_info['life-span'].get('end', 'present')}\n"
                return response
            
            # Fall back to RAG
            return self.generate_response(query)
        
        except Exception as e:
            print(f"Error handling music query: {e}")
            return "I encountered an error processing your request. Please try again."
    
    def chat(self):
        print("Welcome to Enhanced SpotiGPT! Ask me about music, artists, or get recommendations.")
        while True:
            query = input("\nYou: ")
            if query.lower() in ['quit', 'exit']:
                break
            response = self.generate_response(query)
            print(f"\nSpotiGPT: {response}")

if __name__ == "__main__":
    bot = EnhancedMusicChatbot()
    bot.chat()