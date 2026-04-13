"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
from recommender import load_songs, recommend_songs, list_modes


def main() -> None:
    available = list_modes()

    if len(sys.argv) > 1:
        mode_arg = sys.argv[1]
        if mode_arg not in available:
            print(f"Unknown mode '{mode_arg}'.")
            print(f"Available modes: {', '.join(available)}")
            sys.exit(1)
        modes = [mode_arg]
    else:
        modes = available

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
        "likes_mainstream": True,
        "prefers_recent": True,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["synth", "drums"],
        "listening_context": "workout",
        "user_age": 22,
        "favorite_subgenre": "dance pop",
    }

    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["piano", "guitar"],
        "listening_context": "study",
        "user_age": 24,
        "favorite_subgenre": "lo-fi hip hop",
    }

    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["guitar", "drums"],
        "listening_context": "workout",
        "user_age": 26,
        "favorite_subgenre": "hard rock",
    }

    high_energy_sad = {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "likes_mainstream": True,
        "prefers_recent": True,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["synth", "vocals"],
        "listening_context": "commute",
        "user_age": 21,
        "favorite_subgenre": "electropop",
    }

    metal_peaceful = {
        "favorite_genre": "metal",
        "favorite_mood": "peaceful",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": True,
        "preferred_language": "English",
        "preferred_instruments": ["guitar", "bass"],
        "listening_context": "workout",
        "user_age": 28,
        "favorite_subgenre": "death metal",
    }

    acoustic_electronic = {
        "favorite_genre": "electronic",
        "favorite_mood": "focused",
        "target_energy": 0.60,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": True,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["synth", "bass"],
        "listening_context": "study",
        "user_age": 25,
        "favorite_subgenre": "tech house",
    }

    orphan_genre_world = {
        "favorite_genre": "world",
        "favorite_mood": "spiritual",
        "target_energy": 0.40,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": False,
        "preferred_language": "Hindi",
        "preferred_instruments": ["sitar", "tabla"],
        "listening_context": "study",
        "user_age": 32,
        "favorite_subgenre": "Indian classical fusion",
    }

    anti_mainstream_recent = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": True,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["piano", "guitar"],
        "listening_context": "study",
        "user_age": 23,
        "favorite_subgenre": "lo-fi hip hop",
    }

    maximal_indifference = {
        "favorite_genre": "jazz",
        "favorite_mood": "nostalgic",
        "target_energy": 0.50,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
        "allow_explicit": False,
        "preferred_language": "English",
        "preferred_instruments": ["piano", "bass"],
        "listening_context": "study",
        "user_age": 34,
        "favorite_subgenre": "smooth jazz",
    }

    profiles = [
        ("High-Energy Pop", high_energy_pop),
        ("Chill Lofi", chill_lofi),
        ("Deep Intense Rock", deep_intense_rock),
        ("High-Energy + Sad", high_energy_sad),
        ("Metal + Peaceful", metal_peaceful),
        ("Acoustic Electronic", acoustic_electronic),
        ("Orphan Genre (World)", orphan_genre_world),
        ("Anti-Mainstream + Recent", anti_mainstream_recent),
        ("Maximal Indifference", maximal_indifference),
    ]

    for mode in modes:
        print("\n" + "█" * 50)
        print(f"  SCORING MODE: {mode.upper()}")
        print("█" * 50)
        for label, prefs in profiles:
            recommendations = recommend_songs(prefs, songs, k=5, mode=mode)

            print("\n" + "=" * 50)
            print(f"  Top Recommendations — {label}")
            print(f"  Scoring mode: {mode}")
            print("=" * 50)
            for i, (song, score, explanation) in enumerate(recommendations, start=1):
                all_reasons = explanation.split(" | ")
                contributing = [r for r in all_reasons if not r.endswith(": 0.00")]
                zeroed = [r for r in all_reasons if r.endswith(": 0.00")]
                top3 = sorted(contributing, key=lambda r: float(r.split(": ")[1]), reverse=True)[:3]
                no_match = f"  ✗ {', '.join(r.split(' match')[0] for r in zeroed)}" if zeroed else ""
                print(f"  #{i}  {song['title']} by {song['artist']}  [{score:.2f}]")
                print(f"       ↑ {' · '.join(top3)}{no_match}")
            print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
