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
    explicit: int
    language: str
    instruments: str
    listening_context: str
    avg_listener_age: int
    subgenre: str

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
    int_fields = {"id", "popularity", "release_year", "explicit", "avg_listener_age"}
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

SCORING_MODES = {
    "balanced": {
        "genre": 0.25, "energy": 0.20, "valence": 0.15, "mood": 0.08,
        "acousticness": 0.04, "popularity": 0.04, "release_year": 0.04,
        "listening_context": 0.06, "language": 0.05, "instruments": 0.04,
        "subgenre": 0.03, "explicit": 0.01, "avg_listener_age": 0.01,
    },
    "genre_first": {
        "genre": 0.40, "energy": 0.15, "valence": 0.10, "mood": 0.05,
        "acousticness": 0.03, "popularity": 0.03, "release_year": 0.02,
        "listening_context": 0.04, "language": 0.05, "instruments": 0.03,
        "subgenre": 0.08, "explicit": 0.01, "avg_listener_age": 0.01,
    },
    "mood_first": {
        "genre": 0.15, "energy": 0.12, "valence": 0.20, "mood": 0.20,
        "acousticness": 0.02, "popularity": 0.02, "release_year": 0.01,
        "listening_context": 0.15, "language": 0.05, "instruments": 0.03,
        "subgenre": 0.03, "explicit": 0.01, "avg_listener_age": 0.01,
    },
    "energy_focused": {
        "genre": 0.12, "energy": 0.35, "valence": 0.10, "mood": 0.10,
        "acousticness": 0.02, "popularity": 0.01, "release_year": 0.01,
        "listening_context": 0.17, "language": 0.03, "instruments": 0.05,
        "subgenre": 0.02, "explicit": 0.01, "avg_listener_age": 0.01,
    },
}

def list_modes() -> List[str]:
    """Return all available scoring mode names."""
    return list(SCORING_MODES.keys())

def score_song(user_prefs: Dict, song: Dict, weights: Dict) -> Tuple[float, List[str]]:
    """Score a single song against a user profile and return a (total_score, reasons) tuple."""
    reasons = []

    # genre (0.25)
    if user_prefs["favorite_genre"] == song["genre"]:
        genre_score = 1.0
    else:
        genre_score = GENRE_SIMILARITY.get((user_prefs["favorite_genre"], song["genre"]), 0.0)
    reasons.append(f"genre match: {genre_score:.2f}")

    # energy (0.20)
    energy_score = max(0.0, 1.0 - abs(song["energy"] - user_prefs["target_energy"]))
    reasons.append(f"energy match: {energy_score:.2f}")

    # valence (0.15)
    valence_target = MOOD_TO_VALENCE.get(user_prefs["favorite_mood"], 0.5)
    valence_score = max(0.0, 1.0 - abs(song["valence"] - valence_target))
    reasons.append(f"valence match: {valence_score:.2f}")

    # mood (0.08)
    if user_prefs["favorite_mood"] == song["mood"]:
        mood_score = 1.0
    else:
        mood_score = MOOD_SIMILARITY.get((user_prefs["favorite_mood"], song["mood"]), 0.0)
    reasons.append(f"mood match: {mood_score:.2f}")

    # acousticness (0.04)
    ac_target = 0.82 if user_prefs["likes_acoustic"] else 0.15
    acousticness_score = max(0.0, 1.0 - abs(song["acousticness"] - ac_target))
    reasons.append(f"acousticness match: {acousticness_score:.2f}")

    # popularity (0.04)
    pop_target = 0.75 if user_prefs["likes_mainstream"] else 0.25
    popularity_score = max(0.0, 1.0 - abs((song["popularity"] / 100) - pop_target))
    reasons.append(f"popularity match: {popularity_score:.2f}")

    # release_year (0.04)
    year_target = 2023 if user_prefs["prefers_recent"] else 2018
    year_score = max(0.0, 1.0 - abs((song["release_year"] - 2000) / 25 - (year_target - 2000) / 25))
    reasons.append(f"release year match: {year_score:.2f}")

    # explicit (0.01)
    explicit_score = 1.0 if user_prefs["allow_explicit"] or song["explicit"] == 0 else 0.0
    reasons.append(f"explicit match: {explicit_score:.2f}")

    # language (0.05)
    language_score = 1.0 if song["language"] == user_prefs["preferred_language"] else 0.0
    reasons.append(f"language match: {language_score:.2f}")

    # instruments (0.04)
    song_instruments = set(song["instruments"].split("|"))
    preferred = user_prefs["preferred_instruments"]
    if not preferred:
        instruments_score = 0.5
    else:
        instruments_score = min(1.0, len(song_instruments & set(preferred)) / len(preferred))
    reasons.append(f"instruments match: {instruments_score:.2f}")

    # listening_context (0.06)
    context_score = 1.0 if song["listening_context"] == user_prefs["listening_context"] else 0.0
    reasons.append(f"listening context match: {context_score:.2f}")

    # avg_listener_age (0.01)
    age_score = max(0.0, 1.0 - abs(song["avg_listener_age"] - user_prefs["user_age"]) / 30)
    reasons.append(f"listener age match: {age_score:.2f}")

    # subgenre (0.03)
    if song["subgenre"] == user_prefs["favorite_subgenre"]:
        subgenre_score = 1.0
    elif user_prefs["favorite_genre"] in song["subgenre"]:
        subgenre_score = 0.5
    else:
        subgenre_score = 0.0
    reasons.append(f"subgenre match: {subgenre_score:.2f}")

    total_score = (
        genre_score        * weights["genre"] +
        energy_score       * weights["energy"] +
        valence_score      * weights["valence"] +
        mood_score         * weights["mood"] +
        acousticness_score * weights["acousticness"] +
        popularity_score   * weights["popularity"] +
        year_score         * weights["release_year"] +
        explicit_score     * weights["explicit"] +
        language_score     * weights["language"] +
        instruments_score  * weights["instruments"] +
        context_score      * weights["listening_context"] +
        age_score          * weights["avg_listener_age"] +
        subgenre_score     * weights["subgenre"]
    )

    return total_score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    artist_penalty: float = 0.80,
    genre_penalty: float = 0.90,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank them, and return the top-k as (song, score, explanation) tuples.

    artist_penalty: multiplier applied per additional appearance of the same artist (default 0.80).
    genre_penalty:  multiplier applied per additional appearance of the same genre  (default 0.90).
    Both penalties stack cumulatively — the more an artist/genre repeats, the lower the score gets.
    First appearance of any artist or genre is never penalized.
    """
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    scored = [(song, *score_song(user_prefs, song, weights)) for song in songs]
    ranked = sorted(scored, key=lambda x: (-x[1], x[0]["id"]))

    selected = []
    artist_counts = {}
    genre_counts = {}

    for song, score, reasons in ranked:
        if len(selected) == k:
            break
        # penalty compounds with each repeat: 0.80^n for artist, 0.90^n for genre
        # first occurrence (count=0) → multiplier = 1.0, no penalty
        a_count = artist_counts.get(song["artist"], 0)
        g_count = genre_counts.get(song["genre"], 0)
        multiplier = (artist_penalty ** a_count) * (genre_penalty ** g_count)
        penalized_score = score * multiplier
        selected.append((song, penalized_score, " | ".join(reasons)))
        artist_counts[song["artist"]] = a_count + 1
        genre_counts[song["genre"]] = g_count + 1

    return selected
