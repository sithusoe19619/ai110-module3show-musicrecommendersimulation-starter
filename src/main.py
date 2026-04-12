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

    # User taste profile — target values for all scoring features
    user_prefs = {
        "favorite_genre": "pop",       # preferred genre
        "favorite_mood": "happy",      # preferred emotional feel
        "target_energy": 0.75,         # moderate-high energy
        "likes_acoustic": False,       # prefers electric/produced sound
        "likes_mainstream": True,      # prefers popular tracks
        "prefers_recent": True,        # prefers recent releases
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Top Recommendations")
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
