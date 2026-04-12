"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
        "likes_mainstream": True,
        "prefers_recent": True,
    }

    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
    }

    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "likes_mainstream": False,
        "prefers_recent": False,
    }

    high_energy_sad = {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "likes_mainstream": True,
        "prefers_recent": True,
    }

    metal_peaceful = {
        "favorite_genre": "metal",
        "favorite_mood": "peaceful",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "likes_mainstream": False,
        "prefers_recent": False,
    }

    acoustic_electronic = {
        "favorite_genre": "electronic",
        "favorite_mood": "focused",
        "target_energy": 0.60,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": True,
    }

    orphan_genre_world = {
        "favorite_genre": "world",
        "favorite_mood": "spiritual",
        "target_energy": 0.40,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
    }

    anti_mainstream_recent = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": True,
    }

    maximal_indifference = {
        "favorite_genre": "jazz",
        "favorite_mood": "nostalgic",
        "target_energy": 0.50,
        "likes_acoustic": True,
        "likes_mainstream": False,
        "prefers_recent": False,
    }

    profiles = [
        ("High-Energy Pop", high_energy_pop),
        ("Chill Lofi", chill_lofi),
        ("Deep Intense Rock", deep_intense_rock),
        ("High-Energy Sad", high_energy_sad),
        ("Metal + Peaceful", metal_peaceful),
        ("Acoustic Electronic", acoustic_electronic),
        ("Orphan Genre (World)", orphan_genre_world),
        ("Anti-Mainstream + Recent", anti_mainstream_recent),
        ("Maximal Indifference", maximal_indifference),
    ]

    for label, prefs in profiles:
        recommendations = recommend_songs(prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  Top Recommendations — {label}")
        print("=" * 50)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Score: {score:.2f}")
            print("    Reasons:")
            for reason in explanation.split(" | "):
                print(f"      - {reason}")
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
