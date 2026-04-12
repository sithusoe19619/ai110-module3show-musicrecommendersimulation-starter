import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int
    release_year: int

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    likes_mainstream: bool = True
    prefers_recent: bool = True

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    int_fields = {"id", "popularity", "release_year"}
    float_fields = {"energy", "valence", "danceability", "acousticness", "tempo_bpm"}
    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            songs.append(row)
    return songs

MOOD_TO_VALENCE = {
    "happy": 0.80, "chill": 0.62, "intense": 0.63, "relaxed": 0.72,
    "focused": 0.58, "moody": 0.45, "sad": 0.30, "nostalgic": 0.65,
    "energetic": 0.75, "playful": 0.85, "peaceful": 0.58, "confident": 0.70,
    "melancholy": 0.40, "spiritual": 0.63, "dark": 0.25, "aggressive": 0.30,
}

GENRE_SIMILARITY = {
    ("pop", "indie pop"): 0.80, ("indie pop", "pop"): 0.80,
    ("pop", "funk"): 0.50, ("funk", "pop"): 0.50,
    ("pop", "hip-hop"): 0.45, ("hip-hop", "pop"): 0.45,
    ("pop", "electronic"): 0.40, ("electronic", "pop"): 0.40,
    ("pop", "synthwave"): 0.40, ("synthwave", "pop"): 0.40,
    ("pop", "dance"): 0.60, ("dance", "pop"): 0.60,
    ("lofi", "ambient"): 0.65, ("ambient", "lofi"): 0.65,
    ("lofi", "jazz"): 0.50, ("jazz", "lofi"): 0.50,
    ("lofi", "classical"): 0.45, ("classical", "lofi"): 0.45,
    ("lofi", "dream pop"): 0.55, ("dream pop", "lofi"): 0.55,
    ("rock", "metal"): 0.60, ("metal", "rock"): 0.60,
    ("rock", "industrial"): 0.45, ("industrial", "rock"): 0.45,
    ("rock", "punk"): 0.70, ("punk", "rock"): 0.70,
    ("rock", "emo"): 0.50, ("emo", "rock"): 0.50,
    ("rock", "synthwave"): 0.35, ("synthwave", "rock"): 0.35,
    ("electronic", "synthwave"): 0.70, ("synthwave", "electronic"): 0.70,
    ("electronic", "industrial"): 0.60, ("industrial", "electronic"): 0.60,
    ("electronic", "hip-hop"): 0.40, ("hip-hop", "electronic"): 0.40,
    ("jazz", "classical"): 0.45, ("classical", "jazz"): 0.45,
    ("jazz", "funk"): 0.55, ("funk", "jazz"): 0.55,
    ("jazz", "ambient"): 0.30, ("ambient", "jazz"): 0.30,
    ("jazz", "world"): 0.35, ("world", "jazz"): 0.35,
    ("ambient", "classical"): 0.55, ("classical", "ambient"): 0.55,
    ("ambient", "dream pop"): 0.50, ("dream pop", "ambient"): 0.50,
    ("folk", "classical"): 0.40, ("classical", "folk"): 0.40,
    ("folk", "world"): 0.45, ("world", "folk"): 0.45,
    ("folk", "acoustic"): 0.70, ("acoustic", "folk"): 0.70,
    ("folk", "indie pop"): 0.45, ("indie pop", "folk"): 0.45,
    ("hip-hop", "funk"): 0.55, ("funk", "hip-hop"): 0.55,
    ("hip-hop", "industrial"): 0.30, ("industrial", "hip-hop"): 0.30,
    ("metal", "industrial"): 0.55, ("industrial", "metal"): 0.55,
    ("metal", "emo"): 0.40, ("emo", "metal"): 0.40,
    ("dream pop", "indie pop"): 0.60, ("indie pop", "dream pop"): 0.60,
}

MOOD_SIMILARITY = {
    ("happy", "playful"): 0.70, ("playful", "happy"): 0.70,
    ("happy", "energetic"): 0.55, ("energetic", "happy"): 0.55,
    ("happy", "relaxed"): 0.40, ("relaxed", "happy"): 0.40,
    ("chill", "relaxed"): 0.75, ("relaxed", "chill"): 0.75,
    ("chill", "peaceful"): 0.65, ("peaceful", "chill"): 0.65,
    ("chill", "melancholy"): 0.30, ("melancholy", "chill"): 0.30,
    ("intense", "aggressive"): 0.70, ("aggressive", "intense"): 0.70,
    ("intense", "energetic"): 0.65, ("energetic", "intense"): 0.65,
    ("intense", "confident"): 0.45, ("confident", "intense"): 0.45,
    ("intense", "dark"): 0.40, ("dark", "intense"): 0.40,
    ("moody", "melancholy"): 0.65, ("melancholy", "moody"): 0.65,
    ("moody", "sad"): 0.55, ("sad", "moody"): 0.55,
    ("moody", "dark"): 0.50, ("dark", "moody"): 0.50,
    ("moody", "nostalgic"): 0.35, ("nostalgic", "moody"): 0.35,
    ("sad", "melancholy"): 0.80, ("melancholy", "sad"): 0.80,
    ("sad", "nostalgic"): 0.40, ("nostalgic", "sad"): 0.40,
    ("nostalgic", "relaxed"): 0.30, ("relaxed", "nostalgic"): 0.30,
    ("nostalgic", "peaceful"): 0.35, ("peaceful", "nostalgic"): 0.35,
    ("energetic", "confident"): 0.55, ("confident", "energetic"): 0.55,
    ("energetic", "aggressive"): 0.45, ("aggressive", "energetic"): 0.45,
    ("playful", "energetic"): 0.45, ("energetic", "playful"): 0.45,
    ("peaceful", "spiritual"): 0.60, ("spiritual", "peaceful"): 0.60,
    ("focused", "spiritual"): 0.30, ("spiritual", "focused"): 0.30,
    ("dark", "aggressive"): 0.60, ("aggressive", "dark"): 0.60,
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against a user profile and return a (total_score, reasons) tuple."""
    reasons = []

    # genre (0.30)
    if user_prefs["favorite_genre"] == song["genre"]:
        genre_score = 1.0
    else:
        genre_score = GENRE_SIMILARITY.get((user_prefs["favorite_genre"], song["genre"]), 0.0)
    reasons.append(f"genre match: {genre_score:.2f}")

    # energy (0.25)
    energy_score = max(0.0, 1.0 - abs(song["energy"] - user_prefs["target_energy"]))
    reasons.append(f"energy match: {energy_score:.2f}")

    # valence (0.20)
    valence_target = MOOD_TO_VALENCE.get(user_prefs["favorite_mood"], 0.5)
    valence_score = max(0.0, 1.0 - abs(song["valence"] - valence_target))
    reasons.append(f"valence match: {valence_score:.2f}")

    # mood (0.10)
    if user_prefs["favorite_mood"] == song["mood"]:
        mood_score = 1.0
    else:
        mood_score = MOOD_SIMILARITY.get((user_prefs["favorite_mood"], song["mood"]), 0.0)
    reasons.append(f"mood match: {mood_score:.2f}")

    # acousticness (0.05)
    ac_target = 0.82 if user_prefs["likes_acoustic"] else 0.15
    acousticness_score = max(0.0, 1.0 - abs(song["acousticness"] - ac_target))
    reasons.append(f"acousticness match: {acousticness_score:.2f}")

    # popularity (0.05)
    pop_target = 0.75 if user_prefs["likes_mainstream"] else 0.25
    popularity_score = max(0.0, 1.0 - abs((song["popularity"] / 100) - pop_target))
    reasons.append(f"popularity match: {popularity_score:.2f}")

    # release_year (0.05)
    year_target = 2023 if user_prefs["prefers_recent"] else 2018
    year_score = max(0.0, 1.0 - abs((song["release_year"] - 2000) / 25 - (year_target - 2000) / 25))
    reasons.append(f"release year match: {year_score:.2f}")

    total_score = (
        genre_score * 0.30 +
        energy_score * 0.25 +
        valence_score * 0.20 +
        mood_score * 0.10 +
        acousticness_score * 0.05 +
        popularity_score * 0.05 +
        year_score * 0.05
    )

    return total_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank them, and return the top-k as (song, score, explanation) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda x: (-x[1], x[0]["id"]))
    return [(song, score, " | ".join(reasons)) for song, score, reasons in ranked[:min(k, len(songs))]]
