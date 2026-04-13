---
name: Scoring Implementation
description: score_song function signature, weights, lookup tables, and component formulas as implemented in recommender.py
type: project
---

score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]] is implemented in src/recommender.py above recommend_songs.

Weights (sum to 1.0):
- genre: 0.30
- energy: 0.25
- valence: 0.20
- mood: 0.10
- acousticness: 0.05
- popularity: 0.05
- release_year: 0.05

Component formulas:
- genre_score: 1.0 if exact match, else GENRE_SIMILARITY.get((user_genre, song_genre), 0.0)
- energy_score: 1.0 - abs(song["energy"] - user_prefs["target_energy"])
- valence_score: 1.0 - abs(song["valence"] - MOOD_TO_VALENCE.get(user_prefs["favorite_mood"], 0.5))
- mood_score: 1.0 if exact match, else MOOD_SIMILARITY.get((user_mood, song_mood), 0.0)
- acousticness_score: 1.0 - abs(song["acousticness"] - (0.82 if likes_acoustic else 0.15))
- popularity_score: 1.0 - abs((song["popularity"] / 100) - (0.75 if likes_mainstream else 0.25))
- year_score: 1.0 - abs((song["release_year"] - 2000) / 25 - (year_target - 2000) / 25), year_target = 2023 if prefers_recent else 2018

Module-level dicts: MOOD_TO_VALENCE, GENRE_SIMILARITY, MOOD_SIMILARITY — all defined above score_song in recommender.py.
GENRE_SIMILARITY and MOOD_SIMILARITY store all pairs bidirectionally. Exact match is handled in code, not stored.

**Why:** Weighted additive scoring with linear proximity; semantic truth over data-driven patterns.
**How to apply:** Reference these weights and formulas when implementing or verifying recommend_songs or any scoring-related logic.
